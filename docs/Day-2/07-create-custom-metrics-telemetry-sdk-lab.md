# Day 2: Create Custom Metrics Using OCI Telemetry SDKs - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will integrate BharatMart's Prometheus metrics with OCI Monitoring using the OCI Telemetry SDK.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* BharatMart running and exposing metrics at `/metrics` endpoint
* OCI SDK installed (Python or other)
* Access to OCI Console

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Understand how to send custom application metrics to OCI Monitoring
* Use OCI Telemetry SDK to post metrics from BharatMart application
* View custom metrics in OCI Metric Explorer
* Integrate application metrics with infrastructure metrics for complete observability

---

## 2. Background

BharatMart exposes Prometheus-format metrics at `/metrics` endpoint:
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_total` - Request counts with status codes
- `orders_created_total`, `orders_success_total`, `orders_failed_total` - Business metrics
- `payments_processed_total` - Payment metrics

These metrics can be sent to OCI Monitoring as custom metrics using the OCI Telemetry SDK, enabling unified observability.

---

## 3. Hands-On Task 1 — Prepare OCI Configuration

#### Purpose

Set up OCI SDK configuration for posting custom metrics.

### Steps:

1. **Ensure OCI SDK is installed:**
   ```bash
   python3 -c "import oci; print(oci.__version__)"
   ```

2. **Verify OCI configuration:**
   ```bash
   cat ~/.oci/config
   ```
   Should show your tenancy OCID, user OCID, region, etc.

3. **Get Compartment OCID:**
   ```bash
   oci iam compartment list --compartment-id-in-subtree true --all | grep "<your-compartment-name>"
   ```
   Note the compartment OCID for later use.

---

## 4. Hands-On Task 2 — Create Script to Post Custom Metrics

#### Purpose

Create a Python script that reads BharatMart metrics and posts them to OCI Monitoring.

### Steps:

> **📝 Note: Repository Script Available**
> 
> A complete, production-ready version of this script is available in the application repository at `scripts/oci-telemetry-metrics-ingestion.py` with additional features like:
> - Command-line argument parsing (`--compartment-id`, `--metrics-endpoint`, etc.)
> - Enhanced error handling and logging
> - Environment variable support
> - Better Prometheus metric parsing
> 
> You can use the repository script directly, or follow the steps below to create your own version (recommended for learning).
> 
> **To use the repository script:**
> ```bash
> export OCI_COMPARTMENT_ID=ocid1.compartment.oc1...
> export METRICS_ENDPOINT=http://localhost:3000/metrics
> python3 scripts/oci-telemetry-metrics-ingestion.py
> ```
> 
> See `scripts/oci-telemetry-metrics-ingestion.py` for full documentation.

1. **Create metrics ingestion script:**

   Create your own script to learn the implementation details:
   ```bash
   cat > ~/bharatmart-metrics-to-oci.py << 'EOF'
   #!/usr/bin/env python3
   import oci
   import requests
   import re
   from datetime import datetime
   import time
   
   # Load OCI config
   config = oci.config.from_file()
   monitoring = oci.monitoring.MonitoringClient(config)
   
   # Configuration
   COMPARTMENT_OCID = "<your-compartment-ocid>"
   METRICS_ENDPOINT = "http://localhost:3000/metrics"
   NAMESPACE = "custom.bharatmart"
   
   def parse_prometheus_metrics(prometheus_text):
       """Parse Prometheus format metrics from /metrics endpoint"""
       metrics = {}
       for line in prometheus_text.split('\n'):
           if line.startswith('#') or not line.strip():
               continue
           
           # Parse metric line: name{labels} value timestamp
           match = re.match(r'(\w+)(?:\{([^}]+)\})?\s+([\d.]+)', line)
           if match:
               name = match.group(1)
               labels = match.group(2) if match.group(2) else ""
               value = float(match.group(3))
               
               metrics[name] = {
                   'value': value,
                   'labels': labels
               }
       return metrics
   
   def post_metric_to_oci(metric_name, value, dimensions=None):
       """Post a single metric to OCI Monitoring"""
       if dimensions is None:
           dimensions = {}
       
       metric_data = oci.monitoring.models.MetricData(
           namespace=NAMESPACE,
           name=metric_name,
           dimensions=dimensions,
           datapoints=[
               oci.monitoring.models.Datapoint(
                   timestamp=datetime.utcnow(),
                   value=value
               )
           ]
       )
       
       post_metric_details = oci.monitoring.models.PostMetricDataDetails(
           metric_data=[metric_data]
       )
       
       try:
           response = monitoring.post_metric_data(
               post_metric_data_details=post_metric_details,
               compartment_id=COMPARTMENT_OCID
           )
           print(f"Posted {metric_name} = {value}")
           return response
       except Exception as e:
           print(f"Error posting {metric_name}: {e}")
           return None
   
   def main():
       print("Fetching metrics from BharatMart...")
       response = requests.get(METRICS_ENDPOINT)
       
       if response.status_code != 200:
           print(f"Error fetching metrics: {response.status_code}")
           return
       
       metrics = parse_prometheus_metrics(response.text)
       
       # Post key metrics to OCI Monitoring
       print(f"\nPosting metrics to OCI Monitoring (namespace: {NAMESPACE})...")
       
       # HTTP Request Duration (latency)
       if 'http_request_duration_seconds_sum' in metrics:
           latency_sum = metrics['http_request_duration_seconds_sum']['value']
           if 'http_request_duration_seconds_count' in metrics:
               count = metrics['http_request_duration_seconds_count']['value']
               if count > 0:
                   avg_latency = latency_sum / count
                   post_metric_to_oci('api_latency_seconds', avg_latency)
       
       # HTTP Requests Total (by status code)
       for metric_name, metric_data in metrics.items():
           if metric_name.startswith('http_requests_total'):
               value = metric_data['value']
               # Extract status code from labels if present
               dimensions = {}
               labels = metric_data['labels']
               if labels:
                   for label_pair in labels.split(','):
                       if '=' in label_pair:
                           k, v = label_pair.split('=')
                           dimensions[k.strip()] = v.strip().strip('"')
               
               post_metric_to_oci('http_requests_total', value, dimensions)
       
       # Business metrics
       for metric_name in ['orders_created_total', 'orders_success_total', 'orders_failed_total']:
           if metric_name in metrics:
               post_metric_to_oci(metric_name, metrics[metric_name]['value'])
       
       print("\nMetrics posted successfully!")
   
   if __name__ == '__main__':
       main()
   EOF
   ```

2. **Update compartment OCID in script:**
   ```bash
   sed -i "s|<your-compartment-ocid>|$(oci iam compartment list --compartment-id-in-subtree true --all --query 'data[?name==\"<your-compartment>\"].id' --raw-output)|" ~/bharatmart-metrics-to-oci.py
   ```

3. **Make script executable:**
   ```bash
   chmod +x ~/bharatmart-metrics-to-oci.py
   ```

---

## 5. Hands-On Task 3 — Run Metrics Ingestion Script

#### Purpose

Execute the script to post BharatMart metrics to OCI Monitoring.

### Steps:

1. **Run the script:**
   ```bash
   python3 ~/bharatmart-metrics-to-oci.py
   ```

2. **Verify output:**
   Should see messages like:
   ```
   Fetching metrics from BharatMart...
   Posting metrics to OCI Monitoring (namespace: custom.bharatmart)...
   Posted api_latency_seconds = 0.123
   Posted http_requests_total = 1500
   Posted orders_created_total = 45
   Metrics posted successfully!
   ```

3. **Set up periodic execution (optional):**
   ```bash
   # Add to crontab to run every 1 minute
   crontab -e
   # Add line:
   */1 * * * * /usr/bin/python3 ~/bharatmart-metrics-to-oci.py >> /var/log/bharatmart-metrics.log 2>&1
   ```

---

## 6. Hands-On Task 4 — View Custom Metrics in OCI Monitoring

#### Purpose

Verify that custom metrics are available in OCI Metric Explorer.

### Steps:

1. **Access Metric Explorer:**
   - Open **OCI Console** → **Observability & Management** → **Monitoring** → **Metric Explorer**

2. **Select Custom Namespace:**
   - **Namespace:** `custom.bharatmart`
   - **Compartment:** Select your compartment

3. **View Available Metrics:**
   - Should see metrics like:
     - `api_latency_seconds`
     - `http_requests_total`
     - `orders_created_total`
     - `orders_success_total`
     - `orders_failed_total`

4. **Create Query:**
   - Select metric: `api_latency_seconds`
   - View graph showing latency over time

---

## 7. Summary of the Hands-On

Today you:

* Created a script to ingest BharatMart Prometheus metrics into OCI Monitoring
* Used OCI Telemetry SDK to post custom metrics
* Verified custom metrics in OCI Metric Explorer
* Integrated application metrics with infrastructure metrics

These custom metrics enable SLI/SLO definition using actual application behavior.

---

## 8. Next Steps

* Use custom metrics in dashboards (see Dashboard lab)
* Create alarms based on custom metrics
* Define SLIs/SLOs using custom metrics
* Monitor business KPIs (orders, payments) in OCI Monitoring

---

## 9. Solutions Key (Instructor Reference)

### Expected Results:

* Script successfully posts metrics to OCI Monitoring
* Custom metrics visible in Metric Explorer under `custom.bharatmart` namespace
* Metrics updating periodically (if cron job configured)

### Troubleshooting:

* **403 Forbidden:** Check IAM policies allow posting metrics
* **Metrics not appearing:** Wait 1-2 minutes for metrics to be available
* **Connection errors:** Verify OCI config and compartment OCID

