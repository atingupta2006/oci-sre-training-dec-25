#!/usr/bin/env python3
"""
backend-logs-to-oci.py

Tails backend log file (api.log) and sends log lines to OCI Logging.

Features:
- Shared .env file
- Inode-based log rotation detection
- Batching for performance
- Retry with exponential backoff
- Handles JSON + plain-text logs
- Writes internal debug logs to stdout

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
    format="%(asctime)s [%(levelname)s] backend-logs: %(message)s",
)
logger = logging.getLogger("backend-logs")

# -------------------------------------------------------
# Load Shared .env File
# -------------------------------------------------------
ENV_PATH = "./.env"  # Using current directory as per your requirement
load_dotenv(ENV_PATH)

COMPARTMENT_OCID = os.getenv("COMPARTMENT_OCID")
BACKEND_LOG_OCID = os.getenv("BACKEND_LOG_OCID")
BACKEND_LOG_FILE = os.getenv("BACKEND_LOG_FILE")

LOG_BATCH_SIZE = int(os.getenv("LOG_BATCH_SIZE", "50"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))

OCI_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
OCI_REGION = os.getenv("OCI_REGION")

if not BACKEND_LOG_OCID:
    raise RuntimeError("BACKEND_LOG_OCID missing in .env")

if not BACKEND_LOG_FILE:
    raise RuntimeError("BACKEND_LOG_FILE missing in .env")

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
# Helper: Tail file safely with inode detection
# -------------------------------------------------------
def open_log_file(path):
    """
    Opens log file with inode tracking to detect rotation.
    """
    f = open(path, "r")
    st = os.fstat(f.fileno())
    return f, st.st_ino


def detect_rotation(old_file, expected_inode, path):
    """
    Detect if file rotated by comparing inode.
    """
    try:
        st = os.stat(path)
        if st.st_ino != expected_inode:
            logger.warning("Log rotation detected! Reopening file.")
            old_file.close()
            return open_log_file(path)  # new file + new inode
    except FileNotFoundError:
        logger.warning("Log file missing; waiting...")
        time.sleep(1)
    return old_file, expected_inode


# -------------------------------------------------------
# Helper: Send logs to OCI
# -------------------------------------------------------
def send_logs_to_oci(batch):
    if not batch:
        return

    LogEntry = oci.loggingingestion.models.LogEntry
    PutLogsDetails = oci.loggingingestion.models.PutLogsDetails
    LogEntryBatch = oci.loggingingestion.models.LogEntryBatch

    entries = []

    for line in batch:
        # Best effort JSON parsing
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
                type="backend_app",
                subject="api.log",
            )
        ],
    )

    retries = MAX_RETRIES
    for attempt in range(retries):
        try:
            logging_client.put_logs(
                log_id=BACKEND_LOG_OCID,
                put_logs_details=body,
                timestamp_opc_agent_processing=datetime.now(timezone.utc),
            )
            logger.info(f"Sent {len(batch)} logs to OCI")
            return
        except Exception as e:
            delay = 1 * (2**attempt)
            logger.warning(
                f"Error sending logs (attempt {attempt+1}/{retries}): {e}. Retrying {delay}s"
            )
            time.sleep(delay)

    logger.error(f"Failed to send batch after {retries} attempts")


# -------------------------------------------------------
# Main Loop
# -------------------------------------------------------
def main():
    logger.info(f"Starting backend log collector: {BACKEND_LOG_FILE}")

    f, inode = open_log_file(BACKEND_LOG_FILE)

    # Seek to end
    f.seek(0, os.SEEK_END)

    buffer = []

    while True:
        line = f.readline()

        if not line:
            # Idle → check for rotation
            time.sleep(0.5)
            f, inode = detect_rotation(f, inode, BACKEND_LOG_FILE)
            continue

        line = line.rstrip("\n")

        buffer.append(line)

        if len(buffer) >= LOG_BATCH_SIZE:
            send_logs_to_oci(buffer)
            buffer = []


if __name__ == "__main__":
    main()
