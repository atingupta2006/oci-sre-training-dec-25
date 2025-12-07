# Day 5: Use OCI REST APIs to Build an SRE Dashboard - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will use OCI REST APIs to build a custom SRE dashboard.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* OCI CLI configured and working
* OCI Python SDK installed
* Python 3.8+ installed
* Basic understanding of REST APIs and Python
* BharatMart deployed and monitored (from previous days)

**Assumed Deployment:**
* BharatMart application running and monitored
* OCI Monitoring metrics available (infrastructure and custom)
* Monitoring alarms configured
* Load Balancer metrics available

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Understand OCI REST API structure and authentication
* Query OCI Monitoring APIs for metrics
* Retrieve alarm status via APIs
* Build a custom SRE dashboard using API data
* Display SRE metrics programmatically
* Visualize service health and SLI metrics

---

## 2. Background Concepts

### 2.1 OCI REST APIs

**OCI REST APIs** provide programmatic access to all OCI services including Monitoring, Logging, Compute, and more.

**Key Features:**
* RESTful interface (HTTP/HTTPS)
* JSON request/response format
* IAM-based authentication
* Comprehensive service coverage
* Official SDKs available (Python, Java, Go, etc.)

**Use Cases:**
* Custom dashboards and visualizations
* Automated reporting and alerting
* Integration with external tools
* Custom automation workflows
* SRE metric aggregation and display

### 2.2 OCI API Authentication

**Authentication Methods:**
* **API Key Authentication:** For CLI and SDKs
* **Instance Principals:** For Compute instances
* **Service Principals:** For service-to-service calls

**For this lab, we'll use API Key authentication** (configured via `~/.oci/config`).

### 2.3 Dashboard Architecture

```
SRE Dashboard
    ↓ (API Calls)
OCI REST APIs
    ├── Monitoring API (Metrics)
    ├── Monitoring API (Alarms)
    └── Compute API (Instance Status)
    ↓ (JSON Response)
Data Processing
    ↓ (Visualization)
Dashboard Display
```

---

## 3. Hands-On Task 1 — Setup and Configuration

#### Purpose

Set up Python environment and OCI SDK for API access.

### Steps:

#### Step 1: Verify OCI Configuration

1. **Check OCI CLI Configuration:**
   ```bash
   cat ~/.oci/config
   ```

   Should show:
   ```
   [DEFAULT]
   user=ocid1.user.oc1..xxxxx
   fingerprint=xx:xx:xx:xx:xx:xx:xx:xx
   key_file=~/.oci/oci_api_key.pem
   tenancy=ocid1.tenancy.oc1..xxxxx
   region=us-ashburn-1
   ```

2. **Verify OCI CLI Works:**
   ```bash
   oci iam region list
   ```

   Expected: List of available regions

#### Step 2: Verify Python SDK

1. **Check Python Version:**
   ```bash
   python3 --version
   ```

   Expected: Python 3.8 or later

2. **Verify OCI SDK Installation:**
   ```bash
   python3 -c "import oci; print(f'OCI SDK version: {oci.__version__}')"
   ```

   If not installed:
   ```bash
   pip3 install oci --user
   ```

3. **Install Additional Libraries:**
   ```bash
   pip3 install requests matplotlib pandas --user
   ```

#### Step 3: Get Required OCIDs

1. **Get Compartment OCID:**
   ```bash
   oci iam compartment list \
       --compartment-id-in-subtree true \
       --all \
       --query "data[?name=='<your-compartment-name>'].id" \
       --raw-output
   ```

   Save this OCID for later.

2. **List Compute Instances:**
   ```bash
   oci compute instance list \
       --compartment-id <compartment-ocid> \
       --query "data[*].[id, display-name]" \
       --output table
   ```

   Note instance OCIDs and names.

3. **List Monitoring Alarms:**
   ```bash
   oci monitoring alarm list \
       --compartment-id <compartment-ocid> \
       --query "data[*].[id, display-name, is-enabled]" \
       --output table
   ```

   Note alarm OCIDs.

---

## 4. Hands-On Task 2 — Query Metrics via API

#### Purpose

Retrieve metrics from OCI Monitoring using Python SDK.

> **📝 Note: Complete Repository Scripts Available**
> 
> Pre-built, production-ready scripts are available in the application repository:
> - **SRE Dashboard:** `scripts/oci-rest-api-dashboard/sre-dashboard.py`
>   - Comprehensive real-time dashboard with infrastructure metrics, application metrics, alarm status, and SLO tracking
>   - Auto-refreshes every 30 seconds
>   - Full error handling and logging
> - **Metrics Query Example:** `scripts/oci-rest-api-dashboard/query-metrics.py`
>   - Simple example for querying specific metrics
>   - Environment variable support
>   - Command-line configuration
> - **Documentation:** See `scripts/oci-rest-api-dashboard/README.md` for full usage
> 
> **Quick Start with Repository Scripts:**
> ```bash
> # Set environment variables
> export OCI_COMPARTMENT_OCID=ocid1.compartment.oc1...
> export OCI_INSTANCE_OCID=ocid1.instance.oc1...  # Optional
> 
> # Run comprehensive dashboard
> python3 scripts/oci-rest-api-dashboard/sre-dashboard.py
> 
> # Or run metrics query example
> python3 scripts/oci-rest-api-dashboard/query-metrics.py
> ```
> 
> You can use these repository scripts directly, or follow the steps below to create your own versions (recommended for learning).

### Steps:

#### Step 1: Create Metrics Query Script

1. **Create script file:**

   Create your own script to learn the implementation:
   ```bash
   cat > ~/query-metrics.py << 'EOF'
   #!/usr/bin/env python3
   """
   Query OCI Monitoring metrics via REST API
   """
   import oci
   import json
   from datetime import datetime, timedelta
   
   # Load OCI config
   config = oci.config.from_file()
   
   # Create Monitoring client
   monitoring = oci.monitoring.MonitoringClient(config)
   
   # Configuration
   COMPARTMENT_OCID = "<your-compartment-ocid>"
   NAMESPACE = "oci_computeagent"  # or "custom.bharatmart"
   METRIC_NAME = "CpuUtilization"
   RESOURCE_ID = "<instance-ocid>"  # Optional: filter by instance
   
   def query_metrics(namespace, metric_name, compartment_id, resource_id=None):
       """Query metrics from OCI Monitoring"""
       
       # Calculate time range (last 1 hour)
       end_time = datetime.now()
       start_time = end_time - timedelta(hours=1)
       
       # Build query
       query = f"{namespace}.{metric_name}"
       if resource_id:
           query += f"{{resourceId=\"{resource_id}\"}}"
       
       print(f"Query: {query}")
       print(f"Time Range: {start_time.isoformat()} to {end_time.isoformat()}")
       print("-" * 60)
       
       try:
           # Query metrics
           response = monitoring.summarize_metrics_data(
               compartment_id=compartment_id,
               summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
                   namespace=namespace,
                   query=query,
                   start_time=start_time.isoformat(),
                   end_time=end_time.isoformat(),
                   resolution="1m"  # 1 minute resolution
               )
           )
           
           # Process results
           if response.data:
               for metric in response.data:
                   print(f"\nMetric: {metric.name}")
                   print(f"Namespace: {metric.namespace}")
                   if metric.datapoints:
                       print(f"Data Points: {len(metric.datapoints)}")
                       print("\nRecent Values:")
                       for dp in metric.datapoints[-10:]:  # Last 10 points
                           timestamp = dp.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                           value = dp.value
                           print(f"  {timestamp}: {value}")
                   else:
                       print("No data points available")
           else:
               print("No metrics returned")
               
           return response.data
           
       except oci.exceptions.ServiceError as e:
           print(f"Error querying metrics: {e.message}")
           raise
   
   if __name__ == "__main__":
       print("=== OCI Metrics Query ===")
       print("")
       query_metrics(NAMESPACE, METRIC_NAME, COMPARTMENT_OCID, RESOURCE_ID)
   EOF
   
   chmod +x ~/query-metrics.py
   ```

2. **Update Configuration:**
   - Replace `<your-compartment-ocid>` with your compartment OCID
   - Replace `<instance-ocid>` with an instance OCID (optional)
   - Save and close

#### Step 2: Run Metrics Query

1. **Execute Script:**
   ```bash
   python3 ~/query-metrics.py
   ```

   Expected output:
   ```
   === OCI Metrics Query ===
   
   Query: oci_computeagent.CpuUtilization{resourceId="ocid1.instance..."}
   Time Range: 2024-01-15T09:30:00 to 2024-01-15T10:30:00
   ------------------------------------------------------------
   
   Metric: CpuUtilization
   Namespace: oci_computeagent
   Data Points: 60
   
   Recent Values:
     2024-01-15 10:25:00: 45.2
     2024-01-15 10:26:00: 43.8
     2024-01-15 10:27:00: 47.1
     2024-01-15 10:28:00: 44.5
     2024-01-15 10:29:00: 46.3
     2024-01-15 10:30:00: 45.9
   ```

#### Step 3: Query Custom Metrics

1. **Modify Script for Custom Metrics:**
   ```bash
   # Edit ~/query-metrics.py
   # Change:
   NAMESPACE = "custom.bharatmart"
   METRIC_NAME = "http_request_duration_seconds"  # or other BharatMart metric
   ```

2. **Run Again:**
   ```bash
   python3 ~/query-metrics.py
   ```

---

## 5. Hands-On Task 3 — Query Alarm Status

#### Purpose

Retrieve alarm status and state via API.

### Steps:

#### Step 1: Create Alarm Status Script

1. **Create script:**
   ```bash
   cat > ~/query-alarms.py << 'EOF'
   #!/usr/bin/env python3
   """
   Query OCI Monitoring alarm status
   """
   import oci
   import json
   
   # Load OCI config
   config = oci.config.from_file()
   
   # Create Monitoring client
   monitoring = oci.monitoring.MonitoringClient(config)
   
   # Configuration
   COMPARTMENT_OCID = "<your-compartment-ocid>"
   
   def list_alarms(compartment_id):
       """List all alarms and their status"""
       
       print("=== OCI Alarm Status ===")
       print("")
       
       try:
           # List alarms
           response = monitoring.list_alarms(
               compartment_id=compartment_id
           )
           
           if response.data:
               print(f"Found {len(response.data)} alarms")
               print("-" * 80)
               print(f"{'Name':<40} {'Status':<15} {'State':<15} {'Enabled':<10}")
               print("-" * 80)
               
               for alarm in response.data:
                   status = alarm.lifecycle_state
                   state = alarm.is_enabled
                   enabled = "Yes" if state else "No"
                   print(f"{alarm.display_name:<40} {status:<15} {enabled:<10}")
                   
                   # Get alarm status (firing/ok)
                   try:
                       status_response = monitoring.get_alarm(
                           alarm_id=alarm.id
                       )
                       # Note: Alarm firing state requires checking metric data
                       # For simplicity, showing alarm configuration
                       print(f"  Metric: {status_response.data.metric_compartment_id}")
                       print(f"  Query: {status_response.data.query}")
                   except Exception as e:
                       print(f"  Could not get details: {e}")
                   print()
           else:
               print("No alarms found")
               
       except oci.exceptions.ServiceError as e:
           print(f"Error listing alarms: {e.message}")
           raise
   
   if __name__ == "__main__":
       list_alarms(COMPARTMENT_OCID)
   EOF
   
   chmod +x ~/query-alarms.py
   ```

2. **Update Configuration:**
   - Replace `<your-compartment-ocid>` with your compartment OCID

#### Step 2: Run Alarm Query

1. **Execute Script:**
   ```bash
   python3 ~/query-alarms.py
   ```

   Expected output:
   ```
   === OCI Alarm Status ===
   
   Found 3 alarms
   --------------------------------------------------------------------------------
   Name                                      Status          Enabled    
   --------------------------------------------------------------------------------
   cpu-utilization-alarm                     ACTIVE          Yes        
     Metric: ocid1.compartment...
     Query: CpuUtilization[1m].mean() > 80
   
   memory-utilization-alarm                  ACTIVE          Yes        
     Metric: ocid1.compartment...
     Query: MemoryUtilization[1m].mean() > 85
   ```

---

## 6. Hands-On Task 4 — Build SRE Dashboard

#### Purpose

Create a simple SRE dashboard that displays key metrics and alarm status.

> **📝 Note: Complete Dashboard Script Available**
> 
> A comprehensive, production-ready SRE dashboard script is available in the application repository:
> - **Location:** `scripts/oci-rest-api-dashboard/sre-dashboard.py`
> - **Features:** Real-time dashboard with auto-refresh, infrastructure metrics, application metrics, alarm status, SLO tracking
> - **Usage:** `python3 scripts/oci-rest-api-dashboard/sre-dashboard.py`
> - **Documentation:** See `scripts/oci-rest-api-dashboard/README.md`
> 
> You can use the repository script directly, or follow the steps below to create your own version (recommended for learning).

### Steps:

#### Step 1: Create Dashboard Script

1. **Create comprehensive dashboard script:**

   Create your own script to learn the implementation:
   ```bash
   cat > ~/sre-dashboard.py << 'EOF'
   #!/usr/bin/env python3
   """
   SRE Dashboard using OCI REST APIs
   Displays key SRE metrics and alarm status
   """
   import oci
   import json
   from datetime import datetime, timedelta
   import sys
   
   # Load OCI config
   config = oci.config.from_file()
   
   # Create clients
   monitoring = oci.monitoring.MonitoringClient(config)
   compute = oci.core.ComputeClient(config)
   
   # Configuration
   COMPARTMENT_OCID = "<your-compartment-ocid>"
   INSTANCE_OCID = "<instance-ocid>"  # Optional
   
   def get_latest_metric_value(namespace, metric_name, compartment_id, resource_id=None):
       """Get latest metric value"""
       try:
           end_time = datetime.now()
           start_time = end_time - timedelta(minutes=5)
           
           query = f"{namespace}.{metric_name}"
           if resource_id:
               query += f"{{resourceId=\"{resource_id}\"}}"
           
           response = monitoring.summarize_metrics_data(
               compartment_id=compartment_id,
               summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
                   namespace=namespace,
                   query=query,
                   start_time=start_time.isoformat(),
                   end_time=end_time.isoformat(),
                   resolution="1m"
               )
           )
           
           if response.data and response.data[0].datapoints:
               return response.data[0].datapoints[-1].value
           return None
       except Exception as e:
           return f"Error: {e}"
   
   def get_alarm_summary(compartment_id):
       """Get summary of alarms"""
       try:
           response = monitoring.list_alarms(compartment_id=compartment_id)
           if response.data:
               enabled_count = sum(1 for a in response.data if a.is_enabled)
               return {
                   "total": len(response.data),
                   "enabled": enabled_count,
                   "disabled": len(response.data) - enabled_count
               }
           return {"total": 0, "enabled": 0, "disabled": 0}
       except Exception as e:
           return {"error": str(e)}
   
   def get_instance_status(compartment_id):
       """Get compute instance status"""
       try:
           response = compute.list_instances(compartment_id=compartment_id)
           if response.data:
               running = sum(1 for i in response.data if i.lifecycle_state == "RUNNING")
               return {
                   "total": len(response.data),
                   "running": running,
                   "stopped": len(response.data) - running
               }
           return {"total": 0, "running": 0, "stopped": 0}
       except Exception as e:
           return {"error": str(e)}
   
   def display_dashboard():
       """Display SRE Dashboard"""
       print("=" * 80)
       print(" " * 25 + "SRE DASHBOARD")
       print("=" * 80)
       print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
       print()
       
       # Infrastructure Metrics
       print("-" * 80)
       print("INFRASTRUCTURE METRICS")
       print("-" * 80)
       
       cpu = get_latest_metric_value(
           "oci_computeagent", "CpuUtilization", 
           COMPARTMENT_OCID, INSTANCE_OCID
       )
       print(f"CPU Utilization: {cpu}%")
       
       memory = get_latest_metric_value(
           "oci_computeagent", "MemoryUtilization",
           COMPARTMENT_OCID, INSTANCE_OCID
       )
       print(f"Memory Utilization: {memory}%")
       
       # Application Metrics (if available)
       print()
       print("-" * 80)
       print("APPLICATION METRICS (BharatMart)")
       print("-" * 80)
       
       # Try to get custom metrics
       latency = get_latest_metric_value(
           "custom.bharatmart", "http_request_duration_seconds",
           COMPARTMENT_OCID
       )
       if latency:
           print(f"API Latency (avg): {latency:.3f}s")
       else:
           print("API Latency: Not available")
       
       # Service Health
       print()
       print("-" * 80)
       print("SERVICE HEALTH")
       print("-" * 80)
       
       instance_status = get_instance_status(COMPARTMENT_OCID)
       print(f"Compute Instances: {instance_status.get('running', 0)}/{instance_status.get('total', 0)} running")
       
       # Alarm Status
       print()
       print("-" * 80)
       print("ALARM STATUS")
       print("-" * 80)
       
       alarm_summary = get_alarm_summary(COMPARTMENT_OCID)
       print(f"Total Alarms: {alarm_summary.get('total', 0)}")
       print(f"Enabled: {alarm_summary.get('enabled', 0)}")
       print(f"Disabled: {alarm_summary.get('disabled', 0)}")
       
       # SLO Status (Example)
       print()
       print("-" * 80)
       print("SLO STATUS (Example)")
       print("-" * 80)
       
       # Calculate availability (example)
       if instance_status.get('running', 0) > 0:
           availability = (instance_status.get('running', 0) / instance_status.get('total', 1)) * 100
           print(f"Availability: {availability:.2f}%")
           print(f"SLO Target: 99.9%")
           if availability >= 99.9:
               print("Status: ✅ Meeting SLO")
           else:
               print("Status: ⚠️  SLO Breach")
       
       print()
       print("=" * 80)
   
   if __name__ == "__main__":
       try:
           display_dashboard()
       except KeyboardInterrupt:
           print("\nDashboard closed")
           sys.exit(0)
       except Exception as e:
           print(f"Error displaying dashboard: {e}")
           sys.exit(1)
   EOF
   
   chmod +x ~/sre-dashboard.py
   ```

2. **Update Configuration:**
   - Replace `<your-compartment-ocid>` with your compartment OCID
   - Replace `<instance-ocid>` with an instance OCID (or remove if querying all)

#### Step 2: Run Dashboard

1. **Execute Dashboard:**
   ```bash
   python3 ~/sre-dashboard.py
   ```

   Expected output:
   ```
   ================================================================================
                            SRE DASHBOARD
   ================================================================================
   Generated: 2024-01-15 10:30:00
   
   --------------------------------------------------------------------------------
   INFRASTRUCTURE METRICS
   --------------------------------------------------------------------------------
   CPU Utilization: 45.2%
   Memory Utilization: 62.3%
   
   --------------------------------------------------------------------------------
   APPLICATION METRICS (BharatMart)
   --------------------------------------------------------------------------------
   API Latency (avg): 0.145s
   
   --------------------------------------------------------------------------------
   SERVICE HEALTH
   --------------------------------------------------------------------------------
   Compute Instances: 2/2 running
   
   --------------------------------------------------------------------------------
   ALARM STATUS
   --------------------------------------------------------------------------------
   Total Alarms: 5
   Enabled: 5
   Disabled: 0
   
   --------------------------------------------------------------------------------
   SLO STATUS (Example)
   --------------------------------------------------------------------------------
   Availability: 100.00%
   SLO Target: 99.9%
   Status: ✅ Meeting SLO
   
   ================================================================================
   ```

#### Step 3: Create Refreshing Dashboard (Optional)

1. **Create Auto-Refresh Version:**
   ```bash
   cat > ~/sre-dashboard-live.py << 'EOF'
   #!/usr/bin/env python3
   """Live refreshing SRE Dashboard"""
   import time
   import os
   
   # Import dashboard function from previous script
   # (Copy display_dashboard function here or import)
   
   def clear_screen():
       os.system('clear' if os.name == 'posix' else 'cls')
   
   if __name__ == "__main__":
       try:
           while True:
               clear_screen()
               # display_dashboard()  # Call your dashboard function
               time.sleep(30)  # Refresh every 30 seconds
       except KeyboardInterrupt:
           print("\nDashboard stopped")
   EOF
   ```

---

## 7. Hands-On Task 5 — Create HTML Dashboard (Advanced)

#### Purpose

Create a web-based HTML dashboard for better visualization.

### Steps:

#### Step 1: Create HTML Dashboard Generator

1. **Create script to generate HTML:**
   ```bash
   cat > ~/generate-html-dashboard.py << 'EOF'
   #!/usr/bin/env python3
   """
   Generate HTML SRE Dashboard
   """
   import oci
   from datetime import datetime
   
   # (Include metric query functions from previous scripts)
   
   def generate_html_dashboard():
       """Generate HTML dashboard"""
       
       html = f"""
   <!DOCTYPE html>
   <html>
   <head>
       <title>SRE Dashboard - BharatMart</title>
       <style>
           body {{ font-family: Arial, sans-serif; margin: 20px; }}
           .dashboard {{ max-width: 1200px; margin: 0 auto; }}
           .metric-card {{ 
               border: 1px solid #ddd; 
               border-radius: 5px; 
               padding: 15px; 
               margin: 10px; 
               display: inline-block; 
               min-width: 200px;
           }}
           .metric-value {{ font-size: 24px; font-weight: bold; }}
           .status-ok {{ color: green; }}
           .status-warn {{ color: orange; }}
           .status-error {{ color: red; }}
           h1 {{ text-align: center; }}
           .timestamp {{ text-align: center; color: #666; }}
       </style>
       <meta http-equiv="refresh" content="60">
   </head>
   <body>
       <div class="dashboard">
           <h1>SRE Dashboard - BharatMart</h1>
           <div class="timestamp">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
           
           <h2>Infrastructure Metrics</h2>
           <div class="metric-card">
               <div>CPU Utilization</div>
               <div class="metric-value">{cpu_value}%</div>
           </div>
           <div class="metric-card">
               <div>Memory Utilization</div>
               <div class="metric-value">{memory_value}%</div>
           </div>
           
           <h2>Application Metrics</h2>
           <div class="metric-card">
               <div>API Latency</div>
               <div class="metric-value">{latency_value}s</div>
           </div>
           
           <h2>Service Health</h2>
           <div class="metric-card">
               <div>Running Instances</div>
               <div class="metric-value">{running_instances}/{total_instances}</div>
           </div>
       </div>
   </body>
   </html>
   """
       
       # Query metrics and populate values
       # (Add metric query code here)
       
       # Save HTML file
       with open('sre-dashboard.html', 'w') as f:
           f.write(html)
       
       print("Dashboard generated: sre-dashboard.html")
   
   if __name__ == "__main__":
       generate_html_dashboard()
   EOF
   
   chmod +x ~/generate-html-dashboard.py
   ```

2. **Generate and View:**
   ```bash
   python3 ~/generate-html-dashboard.py
   # Open sre-dashboard.html in browser
   ```

---

## 8. Summary of the Hands-On

In this exercise, you:

* Set up OCI SDK and Python environment
* Queried metrics from OCI Monitoring via REST API
* Retrieved alarm status via API
* Built a custom SRE dashboard using API data
* Displayed key SRE metrics programmatically
* Created visualization for service health

This demonstrates how OCI REST APIs enable custom SRE dashboards and integrations.

---

## 9. Additional Enhancements

Consider adding:

* **Historical Trending:** Chart metrics over time
* **Alert Integration:** Display firing alarms prominently
* **SLO Tracking:** Calculate and display SLO compliance
* **Error Budget:** Show remaining error budget
* **Automated Reporting:** Generate daily/weekly reports
* **Multi-Service View:** Aggregate metrics from multiple services
* **Real-time Updates:** WebSocket integration for live updates

---

## 10. Troubleshooting

### API Authentication Errors

* Verify `~/.oci/config` is properly configured
* Check API key fingerprint matches
* Verify IAM policies allow API access

### No Metrics Returned

* Verify namespace and metric name are correct
* Check time range (metrics may not be available for very recent times)
* Verify compartment OCID is correct

### Permission Denied

* Check IAM policies for Monitoring API access
* Verify compartment permissions
* Ensure user has required permissions

---

## 11. Solutions Key (Instructor Reference)

### ✔ Solution Key — Task 1: Setup

#### Expected Configuration:

* OCI CLI configured
* Python 3.8+ installed
* OCI SDK installed
* Compartment and instance OCIDs obtained

### ✔ Solution Key — Task 2-3: API Queries

#### Expected Results:

* Metrics query returns data points
* Alarm query lists all alarms
* Scripts execute without errors

### ✔ Solution Key — Task 4: Dashboard

#### Expected Results:

* Dashboard displays key metrics
* All sections populated correctly
* Dashboard updates with current data

---

## End of Hands-On Document
