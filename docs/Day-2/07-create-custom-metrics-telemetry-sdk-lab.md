# **Day 2: Create Custom Metrics Using OCI Telemetry SDKs — Hands-On Lab**

### **Audience:** IT Engineers, Developers, SREs

### **Theme:** Exporting Prometheus Metrics to OCI Monitoring

### **Objective:** Build and run a continuous metrics ingestion pipeline

---

# **0. Deployment Assumptions**

This hands-on lab demonstrates how to integrate **BharatMart's Prometheus metrics** with **OCI Monitoring** using the OCI Telemetry SDK.

### **Prerequisites**

* Ubuntu VM with Python 3.8+
* BharatMart backend exposing metrics at:
  `http://<vm-ip>:3000/metrics`
* OCI user credentials configured in `~/.oci/config`
* Internet access to OCI Telemetry ingestion endpoint

---

# **1. Lab Objectives**

By completing this module, learners will:

* Understand Prometheus metric structure
* Parse Prometheus metric families using official parser
* Transform metrics into OCI custom metric format
* Implement a continuous metrics ingestion loop
* Push custom metrics to OCI Monitoring
* Generate realistic traffic to populate time-series data
* View application and business metrics in Metric Explorer

---

# **2. Background**

BharatMart exposes a wide range of operational and business metrics using Prometheus format.

### **Performance Metrics**

* `http_requests_total`
* `http_request_duration_seconds` (histogram)
* `external_call_latency_ms` (histogram)

### **Business Metrics**

* `orders_created_total`
* `orders_success_total`
* `orders_failed_total`
* `payments_processed_total`

### **Resilience Metrics**

* `chaos_events_total`
* `service_restarts_total`

### **System Metrics**

* `simulated_latency_ms`

To make these metrics available in OCI Monitoring, they must be:

1. **Fetched** from the `/metrics` endpoint
2. **Parsed** into metric families
3. **Converted** into OCI Telemetry ingestion format
4. **Continuously pushed** to OCI Monitoring

---

# **3. Hands-On Task 1 — Prepare Environment**

### **Step 1 — Validate OCI Configuration**

```bash
cat ~/.oci/config
```

Ensure the file contains:

* tenancy OCID
* user OCID
* fingerprint
* private key
* region

---

### **Step 2 — Identify the Application Compartment**

```bash
oci iam compartment list --compartment-id-in-subtree true --all
```

Record the compartment OCID of your environment.

---

### **Step 3 — Install Required Python Packages**

```bash
pip install oci prometheus_client requests
```

---

# **4. Hands-On Task 2 — Build Prometheus → OCI Metrics Exporter Script**

This script:

* Fetches Prometheus metrics
* Parses metric families
* Extracts counters and gauges
* Computes averages for histograms from `_sum` and `_count`
* Sends every metric to OCI Monitoring
* Runs continuously every 30 seconds
* Uses namespace `bharatmart` (required — no dots allowed)

---

## **4.1 Create the Exporter Script**

```bash
cat > ~/bharatmart-metrics-to-oci.py << 'EOF'
#!/usr/bin/env python3

import oci
import requests
from datetime import datetime, timezone
from prometheus_client.parser import text_string_to_metric_families

# -------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------
COMPARTMENT_OCID = "<your-compartment-ocid>"
METRICS_ENDPOINT = "http://localhost:3000/metrics"
NAMESPACE = "bharatmart"  # Namespace cannot contain dots

# Load OCI configuration
config = oci.config.from_file()

# Telemetry ingestion endpoint
region = config["region"]
telemetry_endpoint = f"https://telemetry-ingestion.{region}.oraclecloud.com"

monitoring = oci.monitoring.MonitoringClient(
    config,
    service_endpoint=telemetry_endpoint
)

# -------------------------------------------------------
# Publish a single metric to OCI Monitoring
# -------------------------------------------------------
def post_metric_to_oci(name, value, dimensions):
    datapoint = oci.monitoring.models.Datapoint(
        timestamp=datetime.now(timezone.utc),
        value=float(value)
    )

    metric = oci.monitoring.models.MetricDataDetails(
        name=name,
        namespace=NAMESPACE,
        compartment_id=COMPARTMENT_OCID,
        dimensions={k: str(v) for k, v in dimensions.items()},
        datapoints=[datapoint],
    )

    payload = oci.monitoring.models.PostMetricDataDetails(metric_data=[metric])
    monitoring.post_metric_data(post_metric_data_details=payload)

    print(f"[OK] {name}={value} dims={dimensions}")

# -------------------------------------------------------
# Metric Processing Logic
# -------------------------------------------------------
def process_metrics():
    print(f"Fetching metrics from {METRICS_ENDPOINT}")
    response = requests.get(METRICS_ENDPOINT)
    metrics_text = response.text

    families = list(text_string_to_metric_families(metrics_text))
    print(f"Parsed {len(families)} Prometheus metric families.")

    for family in families:
        for sample in family.samples:
            name = sample.name
            value = sample.value
            labels = sample.labels

            # Histogram: compute average from sum and count
            if name.endswith("_sum"):
                base = name[:-4]
                count = next(
                    (s.value for s in family.samples if s.name == base + "_count"), 
                    0
                )
                if count > 0:
                    avg = value / count
                    post_metric_to_oci(f"{base}_avg", avg, labels)
                continue

            # Ignore histogram buckets
            if name.endswith("_bucket"):
                continue

            # Push counters & gauges
            post_metric_to_oci(name, value, labels)

    print("Metrics ingestion cycle complete.")

# -------------------------------------------------------
# Continuous Loop
# -------------------------------------------------------
def main():
    import time
    while True:
        process_metrics()
        time.sleep(10)  # run every 10 seconds

if __name__ == "__main__":
    main()
EOF
```

---

## **4.2 Make Script Executable**

```bash
chmod +x ~/bharatmart-metrics-to-oci.py
```

---

# **5. Hands-On Task 3 — Run Metrics Export Continuously**

The script includes an internal `while True` loop.
It automatically:

* Fetches metrics
* Parses them
* Pushes them to OCI
* Sleeps 30 seconds
* Repeats indefinitely

Run:

```bash
python3 ~/bharatmart-metrics-to-oci.py
```

To run continuously in background:

```bash
nohup python3 ~/bharatmart-metrics-to-oci.py > metrics.log 2>&1 &
```

---

# **6. How the Exporter Handles “New vs Old” Metrics**

A common question is:

> **How does the exporter know which metrics are new and which were already ingested?**

The exporter requires **no state tracking**, because:

### **1. OCI Monitoring treats each timestamp as a new datapoint**

We always send:

```python
timestamp=datetime.now(timezone.utc)
```

Every datapoint is unique.

### **2. Prometheus counters are cumulative**

They always increase, so sending the latest value is correct.

### **3. Gauges represent instantaneous state**

No history required.

### **4. Histogram averages are recomputed fresh each cycle**

### **5. No duplicates are possible**

OCI deduplicates automatically if timestamps match (which they never do).

This is the same approach used by:

* Prometheus exporters
* Datadog agent
* Stackdriver sidecar exporters
* CloudWatch custom metric agents

---

# **7. Hands-On Task 4 — Generate Backend Traffic**

### **Set Backend Endpoint**

```bash
BACKEND="http://<vm-ip>:3000"
```

### **Execute Load Generator**

```bash
for i in {1..1000000}; do
  curl -s -o /dev/null $BACKEND/ 
  curl -s -o /dev/null $BACKEND/health &
  curl -s -o /dev/null $BACKEND/metrics

  curl -s -o /dev/null $BACKEND/api/products
  curl -s -o /dev/null $BACKEND/api/orders
  curl -s -o /dev/null $BACKEND/api/users &
  curl -s -o /dev/null $BACKEND/api/cart &
  curl -s -o /dev/null $BACKEND/api/status

  curl -s -o /dev/null -X POST $BACKEND/api/orders &
  curl -s -o /dev/null -X POST $BACKEND/api/users

  curl -s -o /dev/null $BACKEND/not-found &
  curl -s -o /dev/null $BACKEND/does/not/exist &
  curl -s -o /dev/null $BACKEND/.git/config

  PROD_ID=$(shuf -i 1-500 -n 1)
  curl -s -o /dev/null $BACKEND/api/products/$PROD_ID &

  ((i%200==0)) && wait

done

wait
```

This produces real operational and business metric activity.

---

# **8. Hands-On Task 5 — View Metrics in OCI Monitoring**

Navigate to:

**OCI Console → Observability & Management → Monitoring → Metric Explorer**

### **Namespace**

```
bharatmart
```

### **Examples to explore**

| Metric                              | Interpretation              |
| ----------------------------------- | --------------------------- |
| `http_requests_total`               | Total API traffic           |
| `http_request_duration_seconds_avg` | Avg latency                 |
| `external_call_latency_ms_avg`      | External dependency latency |
| `orders_created_total`              | Order creation rate         |
| `orders_success_total`              | Successful orders           |
| `chaos_events_total`                | Chaos engineering events    |

