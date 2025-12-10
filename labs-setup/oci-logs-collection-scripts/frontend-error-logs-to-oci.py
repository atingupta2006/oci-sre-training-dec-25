#!/usr/bin/env python3
"""
frontend-error-logs-to-oci.py

Tails NGINX error log and ships entries to OCI Logging.

Features:
- Shared .env file
- Inode-based rotation detection
- Simple + reliable tailing
- Batching + exponential backoff retry
- Supports JSON and plaintext logs
- Works perfectly on Oracle Linux 9

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
    format="%(asctime)s [%(levelname)s] nginx-error: %(message)s",
)
logger = logging.getLogger("nginx-error")

# -------------------------------------------------------
# Load shared .env
# -------------------------------------------------------
ENV_PATH = "./.env"
load_dotenv()

COMPARTMENT_OCID = os.getenv("COMPARTMENT_OCID")
NGINX_ERROR_LOG_OCID = os.getenv("NGINX_ERROR_LOG_OCID")
NGINX_ERROR_LOG_FILE = os.getenv("NGINX_ERROR_LOG_FILE")

LOG_BATCH_SIZE = int(os.getenv("LOG_BATCH_SIZE", "50"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))

OCI_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
OCI_REGION = os.getenv("OCI_REGION")

if not NGINX_ERROR_LOG_OCID:
    raise RuntimeError("NGINX_ERROR_LOG_OCID missing in .env")

if not NGINX_ERROR_LOG_FILE:
    raise RuntimeError("NGINX_ERROR_LOG_FILE missing in .env")

# -------------------------------------------------------
# OCI Logging Client Setup
# -------------------------------------------------------
try:
    config = oci.config.from_file(profile_name=OCI_PROFILE)
except Exception as e:
    raise RuntimeError(f"Unable to load OCI config ({OCI_PROFILE}): {e}")

region = OCI_REGION or config.get("region")
if not region:
    raise RuntimeError("Region missing in .env and OCI config")

log_endpoint = f"https://ingestion.logging.{region}.oraclecloud.com"

logging_client = oci.loggingingestion.LoggingClient(
    config,
    service_endpoint=log_endpoint,
)

hostname = socket.gethostname()


# -------------------------------------------------------
# Helper: Open log file with inode tracking
# -------------------------------------------------------
def open_log_file(path):
    f = open(path, "r")
    inode = os.fstat(f.fileno()).st_ino
    return f, inode


# -------------------------------------------------------
# Detect log rotation by inode comparison
# -------------------------------------------------------
def detect_rotation(current_file, expected_inode, path):
    try:
        st = os.stat(path)
        if st.st_ino != expected_inode:
            logger.warning("NGINX error log rotation detected. Reopening file.")
            current_file.close()
            return open_log_file(path)
    except FileNotFoundError:
        logger.warning("NGINX error log missing. Waiting...")
        time.sleep(1)

    return current_file, expected_inode


# -------------------------------------------------------
# Send logs to OCI Logging
# -------------------------------------------------------
def send_logs(batch):
    if not batch:
        return

    LogEntry = oci.loggingingestion.models.LogEntry
    PutLogsDetails = oci.loggingingestion.models.PutLogsDetails
    LogEntryBatch = oci.loggingingestion.models.LogEntryBatch

    entries = []

    for line in batch:
        # Best-effort JSON parsing
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
                type="nginx_error",
                subject="error.log",
            )
        ],
    )

    # Retry with exponential backoff
    for attempt in range(MAX_RETRIES):
        try:
            logging_client.put_logs(
                log_id=NGINX_ERROR_LOG_OCID,
                put_logs_details=body,
                timestamp_opc_agent_processing=datetime.now(timezone.utc),
            )
            logger.info(f"Sent {len(batch)} nginx error logs to OCI")
            return
        except Exception as e:
            delay = 1 * (2**attempt)
            logger.warning(
                f"Error sending logs (attempt {attempt+1}/{MAX_RETRIES}): {e}. Retrying in {delay}s"
            )
            time.sleep(delay)

    logger.error(f"Failed to send nginx error logs after {MAX_RETRIES} attempts")


# -------------------------------------------------------
# Main Loop
# -------------------------------------------------------
def main():
    logger.info(f"Starting NGINX error log shipper: {NGINX_ERROR_LOG_FILE}")

    f, inode = open_log_file(NGINX_ERROR_LOG_FILE)

    # Tail: jump to end of file
    f.seek(0, os.SEEK_END)

    buffer = []

    while True:
        line = f.readline()

        if not line:
            # No new line → check for rotation
            time.sleep(0.5)
            f, inode = detect_rotation(f, inode, NGINX_ERROR_LOG_FILE)
            continue

        line = line.rstrip("\n")
        buffer.append(line)

        if len(buffer) >= LOG_BATCH_SIZE:
            send_logs(buffer)
            buffer = []


if __name__ == "__main__":
    main()
