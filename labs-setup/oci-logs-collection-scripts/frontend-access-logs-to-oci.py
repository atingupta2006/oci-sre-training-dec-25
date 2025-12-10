#!/usr/bin/env python3
"""
frontend-access-logs-to-oci.py
Enhanced with detailed debugging logs.
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
    level=logging.DEBUG,   # CHANGED to DEBUG for deeper visibility
    format="%(asctime)s [%(levelname)s] nginx-access: %(message)s",
)
logger = logging.getLogger("nginx-access")

# -------------------------------------------------------
# Load shared .env
# -------------------------------------------------------
logger.debug(f"Loading environment variables from {os.path.abspath('./.env')}")
load_dotenv()

COMPARTMENT_OCID = os.getenv("COMPARTMENT_OCID")
NGINX_ACCESS_LOG_OCID = os.getenv("NGINX_ACCESS_LOG_OCID")
NGINX_ACCESS_LOG_FILE = os.getenv("NGINX_ACCESS_LOG_FILE")

LOG_BATCH_SIZE = int(os.getenv("LOG_BATCH_SIZE", "50"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))

OCI_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
OCI_REGION = os.getenv("OCI_REGION")

logger.debug(f"Loaded OCI_REGION={OCI_REGION}, LOG_BATCH_SIZE={LOG_BATCH_SIZE}, MAX_RETRIES={MAX_RETRIES}")
logger.debug(f"NGINX_ACCESS_LOG_FILE={NGINX_ACCESS_LOG_FILE}")
logger.debug(f"NGINX_ACCESS_LOG_OCID={NGINX_ACCESS_LOG_OCID}")

if not NGINX_ACCESS_LOG_OCID:
    logger.error("Missing NGINX_ACCESS_LOG_OCID")
    raise RuntimeError("NGINX_ACCESS_LOG_OCID missing in .env")

if not NGINX_ACCESS_LOG_FILE:
    logger.error("Missing NGINX_ACCESS_LOG_FILE")
    raise RuntimeError("NGINX_ACCESS_LOG_FILE missing in .env")

# -------------------------------------------------------
# OCI Logging Ingestion Client (Instance Principals)
# -------------------------------------------------------
logger.debug("Initializing Instance Principals signer...")

try:
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    logger.debug("Instance Principals signer initialized successfully.")
except Exception as e:
    logger.exception("Failed to initialize Instance Principals signer")
    raise RuntimeError(f"Unable to initialize Instance Principals signer: {e}")

region = OCI_REGION or signer.region
logger.debug(f"Using OCI region resolved as: {region}")

if not region:
    raise RuntimeError("Region missing in .env and instance metadata")

log_endpoint = f"https://ingestion.logging.{region}.oraclecloud.com"
logger.info(f"Using OCI Logging endpoint: {log_endpoint}")

logging_client = oci.loggingingestion.LoggingClient(
    config={},
    signer=signer,
    service_endpoint=log_endpoint,
)

hostname = socket.gethostname()
logger.debug(f"Detected hostname: {hostname}")

# -------------------------------------------------------
# Open file with inode tracking
# -------------------------------------------------------
def open_log_file(path):
    logger.debug(f"Opening log file: {path}")
    f = open(path, "r")
    inode = os.fstat(f.fileno()).st_ino
    logger.debug(f"Opened file {path} with inode {inode}")
    return f, inode


# -------------------------------------------------------
# Detect log rotation
# -------------------------------------------------------
def detect_rotation(current_file, expected_inode, path):
    try:
        st = os.stat(path)
        if st.st_ino != expected_inode:
            logger.warning(f"Log rotation detected! Old inode={expected_inode}, new inode={st.st_ino}")
            current_file.close()
            return open_log_file(path)
    except FileNotFoundError:
        logger.warning(f"Log file missing ({path}) — likely during rotation. Retrying...")
        time.sleep(1)

    return current_file, expected_inode


# -------------------------------------------------------
# Push logs to OCI in batches
# -------------------------------------------------------
def send_logs(batch):
    if not batch:
        logger.debug("send_logs called with empty batch — skipping.")
        return

    logger.debug(f"Preparing to send batch of size={len(batch)}")

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

    logger.debug(f"Built OCI log entries count={len(entries)}")

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
            logger.debug(f"Sending batch to OCI (attempt {attempt+1})")
            logging_client.put_logs(
                log_id=NGINX_ACCESS_LOG_OCID,
                put_logs_details=body,
                timestamp_opc_agent_processing=datetime.now(timezone.utc),
            )
            logger.info(f"Successfully sent {len(batch)} logs to OCI")
            return
        except Exception as e:
            delay = 1 * (2 ** attempt)
            logger.warning(f"Error sending logs (attempt {attempt+1}/{MAX_RETRIES}) → {e}")
            logger.debug(f"Retrying after {delay} seconds...")
            time.sleep(delay)

    logger.error("All retries failed — logs were NOT sent to OCI")


# -------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------
def main():
    logger.info(f"Starting NGINX log shipper. File: {NGINX_ACCESS_LOG_FILE}")

    f, inode = open_log_file(NGINX_ACCESS_LOG_FILE)

    # Tail behaviour
    logger.debug("Seeking to end of file...")
    f.seek(0, os.SEEK_END)

    buffer = []

    while True:
        line = f.readline()

        if not line:
            logger.debug("No new log line — sleeping 0.5s")
            time.sleep(0.5)
            f, inode = detect_rotation(f, inode, NGINX_ACCESS_LOG_FILE)
            continue

        cleaned = line.rstrip("\n")
        buffer.append(cleaned)
        logger.debug(f"Buffered line (current batch size={len(buffer)})")

        if len(buffer) >= LOG_BATCH_SIZE:
            logger.debug(f"Batch size reached ({LOG_BATCH_SIZE}). Sending...")
            send_logs(buffer)
            buffer = []


if __name__ == "__main__":
    main()
