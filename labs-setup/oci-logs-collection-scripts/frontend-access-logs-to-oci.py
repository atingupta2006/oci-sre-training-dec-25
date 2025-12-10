#!/usr/bin/env python3
"""
frontend-access-logs-to-oci.py

Tails NGINX access log and ships entries to OCI Logging.

Features:
- Uses shared .env file
- Inode-based log rotation detection
- Fast + stable
- Batching
- Retry with exponential backoff
- Handles JSON + plain-text logs
- Works on Oracle Linux 9

Author: BharatMart Observability
"""

import os
import time
import json
import logging
import socket
from datetime import datetime, timezone

import oci
from dotenv import load_dotenv

# -------------------------------------------------------
# Logging Setup
# -------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] nginx-access: %(message)s",
)
logger = logging.getLogger("nginx-access")

# -------------------------------------------------------
# Load shared .env
# -------------------------------------------------------
ENV_PATH = "./.env"
load_dotenv()

COMPARTMENT_OCID = os.getenv("COMPARTMENT_OCID")
NGINX_ACCESS_LOG_OCID = os.getenv("NGINX_ACCESS_LOG_OCID")
NGINX_ACCESS_LOG_FILE = os.getenv("NGINX_ACCESS_LOG_FILE")

LOG_BATCH_SIZE = int(os.getenv("LOG_BATCH_SIZE", "50"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))

OCI_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
OCI_REGION = os.getenv("OCI_REGION")

if not NGINX_ACCESS_LOG_OCID:
    raise RuntimeError("NGINX_ACCESS_LOG_OCID missing in .env")

if not NGINX_ACCESS_LOG_FILE:
    raise RuntimeError("NGINX_ACCESS_LOG_FILE missing in .env")

# -------------------------------------------------------
# OCI Logging Ingestion Client
# -------------------------------------------------------
# -------------------------------------------------------
# OCI Logging Ingestion Client (Instance Principals)
# -------------------------------------------------------
try:
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
except Exception as e:
    raise RuntimeError(f"Unable to initialize Instance Principals signer: {e}")

region = OCI_REGION or signer.region
if not region:
    raise RuntimeError("Region missing in .env and instance metadata")

log_endpoint = f"https://ingestion.logging.{region}.oraclecloud.com"

logging_client = oci.loggingingestion.LoggingClient(
    config={},
    signer=signer,
    service_endpoint=log_endpoint,
)


hostname = socket.gethostname()


# -------------------------------------------------------
# Helper: open log file with inode tracking
# -------------------------------------------------------
def open_log_file(path):
    f = open(path, "r")
    inode = os.fstat(f.fileno()).st_ino
    return f, inode


# -------------------------------------------------------
# Detect log rotation using inode comparison
# -------------------------------------------------------
def detect_rotation(current_file, expected_inode, path):
    try:
        st = os.stat(path)
        if st.st_ino != expected_inode:
            logger.warning("NGINX access log rotation detected. Reopening file.")
            current_file.close()
            return open_log_file(path)
    except FileNotFoundError:
        logger.warning("NGINX access log missing. Waiting...")
        time.sleep(1)

    return current_file, expected_inode


# -------------------------------------------------------
# Send logs to OCI
# -------------------------------------------------------
def send_logs(batch):
    if not batch:
        return

    LogEntry = oci.loggingingestion.models.LogEntry
    PutLogsDetails = oci.loggingingestion.models.PutLogsDetails
    LogEntryBatch = oci.loggingingestion.models.LogEntryBatch

    entries = []
    for line in batch:
        try:
            parsed = json.loads(line)
            if not isinstance(parsed, dict):
                parsed = {"message": line}
        except Exception:
            parsed = {"message": line}

        entries.append(
            LogEntry(
                data=parsed,
                id=str(time.time_ns()),
                time=datetime.now(timezone.utc).isoformat(),
            )
        )

    body = PutLogsDetails(
        specversion="1.0",
        log_entry_batches=[
            LogEntryBatch(
                entries=entries,
                source=hostname,
                type="nginx_access",
                subject="access.log",
            )
        ],
    )

    # Retry with exponential backoff
    for attempt in range(MAX_RETRIES):
        try:
            logging_client.put_logs(
                log_id=NGINX_ACCESS_LOG_OCID,
                put_logs_details=body,
                timestamp_opc_agent_processing=datetime.now(timezone.utc),
            )
            logger.info(f"Sent {len(batch)} nginx access logs to OCI")
            return
        except Exception as e:
            delay = 1 * (2**attempt)
            logger.warning(
                f"Error sending logs (attempt {attempt+1}/{MAX_RETRIES}): {e}. Retrying {delay}s..."
            )
            time.sleep(delay)

    logger.error(f"Failed after {MAX_RETRIES} retries sending NGINX access logs")


# -------------------------------------------------------
# Main loop
# -------------------------------------------------------
def main():
    logger.info(f"Starting NGINX access log shipper: {NGINX_ACCESS_LOG_FILE}")

    f, inode = open_log_file(NGINX_ACCESS_LOG_FILE)

    # Go to end of file (tail -f behavior)
    f.seek(0, os.SEEK_END)

    buffer = []

    while True:
        line = f.readline()

        if not line:
            # No new data, check for rotation
            time.sleep(0.5)
            f, inode = detect_rotation(f, inode, NGINX_ACCESS_LOG_FILE)
            continue

        line = line.rstrip("\n")
        buffer.append(line)

        if len(buffer) >= LOG_BATCH_SIZE:
            send_logs(buffer)
            buffer = []


if __name__ == "__main__":
    main()
