#!/usr/bin/env python3
"""
backend-metrics-to-oci.py

Scrapes Prometheus metrics from BharatMart backend (/metrics)
and pushes them to OCI Monitoring.

Uses:
- Shared .env file
- OCI Python SDK
- Prometheus text parser
- Multiple namespaces (backend, business)
- Histogram _sum/_count → avg
- Safe batching + retry

Author: BharatMart Observability
"""

import os
import time
import socket
import logging
from datetime import datetime, timezone

import requests
import oci
from dotenv import load_dotenv
from prometheus_client.parser import text_string_to_metric_families

# -------------------------------------------------------
# Logging Setup
# -------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] backend-metrics: %(message)s",
)
logger = logging.getLogger("backend-metrics-to-oci")

# -------------------------------------------------------
# Load Shared .env
# -------------------------------------------------------
ENV_PATH = "/opt/bharatmart-observability/.env"
load_dotenv()

COMPARTMENT_OCID = os.getenv("COMPARTMENT_OCID")
if not COMPARTMENT_OCID:
    raise RuntimeError("COMPARTMENT_OCID missing in .env")

BACKEND_METRICS_ENDPOINT = os.getenv("BACKEND_METRICS_ENDPOINT")
if not BACKEND_METRICS_ENDPOINT:
    raise RuntimeError("BACKEND_METRICS_ENDPOINT missing in .env")

NAMESPACE_BACKEND = os.getenv("METRIC_NAMESPACE_BACKEND", "bharatmart_backend")

SCRAPE_INTERVAL_SECONDS = int(os.getenv("SCRAPE_INTERVAL_SECONDS", "15"))

OCI_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
OCI_REGION = os.getenv("OCI_REGION")  # Optional override

# -------------------------------------------------------
# OCI Monitoring Client Setup
# -------------------------------------------------------
try:
    config = oci.config.from_file(profile_name=OCI_PROFILE)
except Exception as e:
    raise RuntimeError(f"Unable to load OCI config ({OCI_PROFILE}): {e}")

region = OCI_REGION or config.get("region")
if not region:
    raise RuntimeError("Region missing in .env and OCI config")

telemetry_endpoint = f"https://telemetry-ingestion.{region}.oraclecloud.com"

monitoring_client = oci.monitoring.MonitoringClient(
    config,
    service_endpoint=telemetry_endpoint,
)

hostname = socket.gethostname()

MAX_METRIC_STREAMS = 50  # OCI API limit per request


# -------------------------------------------------------
# Scrape Prometheus text
# -------------------------------------------------------
def scrape_metrics():
    logger.info(f"Scraping /metrics from {BACKEND_METRICS_ENDPOINT}")
    resp = requests.get(BACKEND_METRICS_ENDPOINT, timeout=5)
    resp.raise_for_status()
    return resp.text


# -------------------------------------------------------
# Convert Prometheus → OCI Metrics
# -------------------------------------------------------
def convert_prom_to_oci(text_data: str):
    MetricDataDetails = oci.monitoring.models.MetricDataDetails
    Datapoint = oci.monitoring.models.Datapoint

    families = list(text_string_to_metric_families(text_data))
    logger.info(f"Parsed {len(families)} Prometheus metric families")

    metric_payloads = []

    for family in families:
        sum_map = {}
        count_map = {}

        # First pass: collect histogram sums and counts
        for sample in family.samples:
            label_key = tuple(sorted(sample.labels.items()))
            if sample.name.endswith("_sum"):
                sum_map[label_key] = sample.value
            elif sample.name.endswith("_count"):
                count_map[label_key] = sample.value

        # Compute histogram averages
        for labels, total_sum in sum_map.items():
            count = count_map.get(labels)
            if count and count > 0:
                base_name = None
                for sample in family.samples:
                    if sample.name.endswith("_sum") and tuple(
                        sorted(sample.labels.items())
                    ) == labels:
                        base_name = sample.name[:-4]  # strip "_sum"
                        break

                if base_name:
                    metric_name = f"{base_name}_avg"
                    dim = dict(labels)
                    dim["host"] = hostname

                    dp = Datapoint(
                        timestamp=datetime.now(timezone.utc),
                        value=float(total_sum / count),
                    )

                    metric_payloads.append(
                        MetricDataDetails(
                            name=metric_name,
                            namespace=NAMESPACE_BACKEND,
                            compartment_id=COMPARTMENT_OCID,
                            dimensions={k: str(v) for k, v in dim.items()},
                            datapoints=[dp],
                        )
                    )

        # Second pass: counters, gauges, etc.
        for sample in family.samples:
            name = sample.name

            # Skip internal histogram metrics
            if name.endswith("_sum") or name.endswith("_count") or name.endswith(
                "_bucket"
            ):
                continue

            try:
                value = float(sample.value)
            except Exception:
                logger.warning(f"Skipping non-numeric metric: {name}")
                continue

            dimensions = dict(sample.labels)
            dimensions["host"] = hostname

            dp = Datapoint(
                timestamp=datetime.now(timezone.utc),
                value=value,
            )

            metric_payloads.append(
                MetricDataDetails(
                    name=name,
                    namespace=NAMESPACE_BACKEND,
                    compartment_id=COMPARTMENT_OCID,
                    dimensions={k: str(v) for k, v in dimensions.items()},
                    datapoints=[dp],
                )
            )

    logger.info(f"Prepared {len(metric_payloads)} OCI metric streams")
    return metric_payloads


# -------------------------------------------------------
# Send metrics with retry and chunking
# -------------------------------------------------------
def send_metrics(metric_list):
    if not metric_list:
        logger.info("No metrics to send.")
        return

    PostMetricDataDetails = oci.monitoring.models.PostMetricDataDetails

    for i in range(0, len(metric_list), MAX_METRIC_STREAMS):
        chunk = metric_list[i : i + MAX_METRIC_STREAMS]
        payload = PostMetricDataDetails(metric_data=chunk)

        retries = int(os.getenv("MAX_RETRIES", 5))

        for attempt in range(retries):
            try:
                response = monitoring_client.post_metric_data(
                    post_metric_data_details=payload
                )
                failed = response.data.failed_metrics or []
                if failed:
                    logger.warning(
                        f"OCI partial failure: {len(failed)} metrics in this chunk"
                    )
                logger.info(f"Chunk of {len(chunk)} metrics sent successfully.")
                break
            except Exception as e:
                delay = 1 * (2**attempt)
                logger.warning(
                    f"Retry {attempt + 1}/{retries} failed: {e}. Sleeping {delay}s."
                )
                time.sleep(delay)
        else:
            logger.error(
                f"Failed to send metrics chunk after {retries} retries (size {len(chunk)})"
            )


# -------------------------------------------------------
# Run cycle
# -------------------------------------------------------
def run_once():
    try:
        text_data = scrape_metrics()
        metric_list = convert_prom_to_oci(text_data)
        send_metrics(metric_list)
    except Exception as e:
        logger.error(f"Error during cycle: {e}")


# -------------------------------------------------------
# Main Loop
# -------------------------------------------------------
def main():
    logger.info(
        f"Starting backend-metrics collector (namespace={NAMESPACE_BACKEND}, interval={SCRAPE_INTERVAL_SECONDS}s)"
    )

    while True:
        run_once()
        time.sleep(SCRAPE_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
