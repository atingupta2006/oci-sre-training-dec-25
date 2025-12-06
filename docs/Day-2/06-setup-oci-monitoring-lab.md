# Day 2: Set up OCI Monitoring (Metrics Explorer, Alarms) - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will set up OCI Monitoring on your OCI account.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* BharatMart running on OCI Compute instance
* Access to OCI Console

---

## 1. Objective of This Hands-On

By the end of this exercise, learners will:

* Understand how OCI's Monitoring service collects and organizes metrics
* Identify metric namespaces and types
* Differentiate between default and custom metrics
* Enable and view Compute metrics
* Inspect metric names relevant to the BharatMart app environment

This activity connects directly to future topics—SLOs, alerting, dashboards, and incident response.

---

## 2. Quick Overview Before the Hands-On

Students must understand three simple concepts:

### 2.1 Monitoring Service Overview

OCI Monitoring collects time‑series metrics such as:

* CPU utilization
* Memory usage (via custom metrics)
* Disk usage
* Network traffic
* API request counts (if custom metrics are sent)

Metrics are organized and visualized using the **Metric Explorer**.

### 2.2 Metric Namespaces

A *namespace* is a logical group of metrics.
Examples:

* `oci_computeagent` → compute-level metrics
* `oci_vcn` → network-level metrics
* `oci_loadbalancer` → load balancer metrics

Think of namespaces as "folders" that contain related metric names.

### 2.3 Default vs Custom Metrics

* **Default metrics:** automatically collected by OCI

  * CPU Utilization
  * Memory Utilization (for supported shapes)
  * Network Throughput
* **Custom metrics:** sent by your application or scripts

  * API call counts
  * Order placement success rate
  * API latency metrics

**Note:** BharatMart application exposes custom metrics at `/metrics` endpoint:
- `http_request_duration_seconds` - Request latency
- `http_requests_total` - Request counts with status codes
- `orders_created_total`, `orders_success_total`, `orders_failed_total` - Business metrics
- `payments_processed_total` - Payment metrics

These custom metrics can be integrated with OCI Monitoring (see next lab for steps). For this introductory lab, we focus on **default infrastructure metrics** from the Compute instance to understand OCI Monitoring basics.

---

## 3. Hands-On Task 0 — Understand System Configuration

#### Purpose

First, understand what BharatMart application configuration and services are available.

Before setting up monitoring, it's helpful to understand the system configuration. BharatMart provides a system information endpoint that shows deployment details, enabled features, and service health.

### Steps:

1. **Check System Information:**
   ```bash
   curl http://localhost:3000/api/system/info | jq '.'
   ```

2. **View Deployment Configuration:**
   ```bash
   curl http://localhost:3000/api/system/info | jq '.deployment'
   ```

3. **Check Service Health:**
   ```bash
   curl http://localhost:3000/api/system/info | jq '.services'
   ```

4. **View Enabled Features:**
   ```bash
   curl http://localhost:3000/api/system/info | jq '.features'
   ```

#### What this shows

- Deployment mode (single-vm, multi-tier, etc.)
- Database, cache, and worker configurations
- Which observability features are enabled (metrics, logging, tracing)
- Service health status

This information helps you understand what metrics and logs are available for monitoring setup.

---

## 4. Hands-On Task 1 — Enable Metrics for Compute Instance

### Purpose: Ensure your BharatMart app's VM is sending default compute metrics.

Metrics for Compute are enabled automatically **if the OCI Monitoring Agent is installed**. Most images like Oracle Linux include it by default.

### Steps:

1. Open the **Navigation Menu (☰)**.
2. Go to **Compute → Instances**.
3. Click your instance: `*<student-id>-compute-training*`.
4. Open **Monitoring** section.
5. Check **Metrics**.
6. Confirm that graphs for CPU, Network, or Disk are visible.

### What You Should See:

* CPU Utilization graph
* Memory Utilization graph (if supported)
* Network packets/bytes graphs
* Disk throughput graphs

If metrics show data points, monitoring is correctly enabled.

### Why This Matters (SRE Context):

Compute metrics are the first signals SREs check during incidents. They help answer:

* Is the service overloaded?
* Is CPU throttling happening?
* Is network traffic spiking?
* Is the underlying VM healthy?

---

## 5. Hands-On Task 2 — Inspect Available Metric Names

### Purpose: Learn how to explore metric namespaces and names in OCI.

This exercise helps understand how OCI organizes metrics.

### Steps:

1. Open **Navigation Menu → Observability & Management → Monitoring**.
2. Click **Metric Explorer**.
3. In the **Namespace** dropdown, choose:

   * `oci_computeagent`
4. In the **Metric Name** dropdown, review available metrics.

You should see metrics like:

* `CpuUtilization`
* `MemoryUtilization`
* `NetworkBytesIn`
* `NetworkBytesOut`
* `DiskBytesRead`
* `DiskBytesWritten`

#### Student Activity

List the metric names you find.

Use this table:

| Metric Name | Description (Your Notes) |
| ----------- | ------------------------ |
|             |                          |
|             |                          |
|             |                          |

---

## 6. Summary of the Hands-On

Today you:

* Enabled and validated Compute instance metrics
* Explored OCI Monitoring
* Inspected metric namespaces and names
* Prepared for future labs on dashboards, SLO validation, and alerting

These basics are essential for real-time SRE work.

---

## 7. Solutions Key (Instructor Reference)

This section provides sample answers so students can self-check after completing the activity.

### Solution Key — Task 1: Enable Metrics on Compute Instance

#### ✔ What students should observe:

* **CPU Utilization graph visible** → Confirms compute metrics are flowing.
* **Network metrics visible** → Confirms VCN + instance networking is active.
* **Disk I/O visible** → Confirms boot volume metrics are available.
* **Memory Utilization** (only on supported shapes) → It's okay if missing.

#### ✔ Why this is correct:

If any of these graphs are populating with timestamps and data points, it proves:

* The Monitoring agent is installed
* Metrics collection is healthy
* The instance is actively reporting to OCI Monitoring

If graphs show *"No Data"*, students should:

1. Ensure the instance is in **Running** state.
2. Wait 2–5 minutes (metrics are emitted at intervals).
3. Confirm they selected the correct **compartment**.

### Solution Key — Task 2: Inspect Available Metric Names

#### ✔ Expected Namespace:

```
oci_computeagent
```

#### ✔ Expected Metric Names Students Should See:

(Names may vary slightly based on shape/OS.)

| Metric Name          | What It Means                               |
| -------------------- | ------------------------------------------- |
| CpuUtilization       | Percentage of CPU used on the VM            |
| MemoryUtilization    | Percentage of RAM being used (if supported) |
| NetworkBytesIn       | Bytes received by the VM over the network   |
| NetworkBytesOut      | Bytes sent by the VM                        |
| DiskBytesRead        | Boot volume read throughput                 |
| DiskBytesWritten     | Boot volume write throughput                |
| VnicBytesRx          | Incoming bytes on the VNIC                  |
| VnicBytesTx          | Outgoing bytes on the VNIC                  |
| CpuUtilizationPerCpu | CPU usage measured per core                 |

#### ✔ Why these metrics matter for the BharatMart App:

* **CPU** → sudden spikes may indicate overloaded API requests during peak shopping hours.
* **Memory** → memory pressure may cause app slowdowns, impacting order placement latency.
* **Network** → traffic spikes align with peak shopping periods and order placement bursts.
* **Disk I/O** → high values may signal database or logging bottlenecks affecting BharatMart performance.

Students should recognize that these default metrics form the baseline for diagnosing reliability issues. Additionally, BharatMart exposes application-level metrics at the `/metrics` endpoint which complement these infrastructure metrics.

