# Day 2: Create Dashboards and Visualization - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will create monitoring dashboards on your OCI account.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* BharatMart running on OCI Compute instance
* Metrics available (default and/or custom)
* Alarms created (from previous lab)

---

## 1. Objective of This Hands-On

By the end of this exercise, students will:

* Understand how to create and organize an OCI Dashboard
* Build visual panels for latency and uptime metrics
* Add alarm widgets to unify alert visibility
* Interpret metrics in the context of reliability and SLOs

This is foundational for later topics: SLO validation, alert tuning, and incident review.

---

## 2. Background Before Hands-On

Students should recall:

### 2.1 Dashboards Overview

OCI Dashboards allow you to visualize:

* Compute metrics (CPU, memory, network)
* Custom metrics (latency, errors, business KPIs)
* Alarms firing states
* Logs & traces (via widgets)

Dashboards help SREs:

* Validate SLO performance
* Spot patterns and anomalies
* Investigate incidents

### 2.2 SLO-Focused Panels

SRE dashboards prioritize panels that show:

* **User-visible performance** → latency, success rate
* **Error patterns** → 5xx spikes, anomalies
* **Service uptime** → availability indicators
* **Burn rate** (later)

This hands-on focuses on the first two.

---

## 3. Hands-On Task 1 — Build a Dashboard for Latency & Uptime

#### Purpose

Create a clear view of how the system is performing.

You will build **essential panels**:

1. **Latency panel** using BharatMart custom metrics from `/metrics` endpoint (`http_request_duration_seconds`)
2. **Error rate panel** using BharatMart custom metrics (`http_requests_total`)
3. **Uptime panel** (instance state + health)
4. **Infrastructure panels** (CPU, Network) as complementary metrics

### Steps:

1. Open **Navigation Menu (☰) → Observability & Management → Dashboards**.
2. Click **Create Dashboard**.
3. Enter:

   * **Name:** `<student-id>-sre-dashboard`
   * **Compartment:** your training compartment
4. Click **Create**.

You will now land in an empty dashboard.

---

## A. Add Latency Panel Using BharatMart Custom Metrics

BharatMart exposes Prometheus metrics at `/metrics` endpoint. These **custom metrics are the primary source** for application-level observability:

- `http_request_duration_seconds` - HTTP request latency (histogram) - **Primary for latency monitoring**
- `http_requests_total` - Request counts with status codes - **Primary for error rate monitoring**
- `orders_created_total`, `orders_success_total`, `orders_failed_total` - Business metrics
- `payments_processed_total` - Payment metrics

#### Prerequisite

BharatMart metrics must be integrated with OCI Monitoring as custom metrics (namespace: `custom.bharatmart`). See previous lab for integration steps.

### Steps to Add Latency Panel:

1. Click **Add Widget → Metric Chart**.
2. In **Metric Namespace**, choose: `custom.bharatmart`
3. Under **Metric Name**, select: `api_latency_seconds` or `http_request_duration_seconds`
4. Configure the chart:
   - **Statistic:** `Mean` or `P99`
   - **Interval:** `1 minute`
5. Title it: **"BharatMart API Latency (P95/P99)"**
6. Click **Create**.

### Steps to Add Error Rate Panel:

1. Click **Add Widget → Metric Chart**.
2. In **Metric Namespace**, choose: `custom.bharatmart`
3. Under **Metric Name**, select: `http_requests_total`
4. Configure to show error rate:
   - Filter by status_code dimension if available
   - Or use separate panels for 2xx vs 5xx requests
5. Title it: **"BharatMart Error Rate"**
6. Click **Create**.

### Steps to Add Infrastructure Metrics (Complementary):

For infrastructure-level visibility, add **CPU and Network activity** as complementary panels:

1. Click **Add Widget → Metric Chart**.
2. In **Metric Namespace**, choose: `oci_computeagent`
3. Under **Metric Name**, select: `CpuUtilization`
4. Select your instance: `<student-id>-compute-training`
5. Title it: **"CPU Utilization (Infrastructure)"**
6. Click **Create**.

Repeat to add **NetworkBytesIn** or **NetworkBytesOut** panel.
These infrastructure metrics complement application metrics by showing resource usage.

---

## B. Add Uptime Panel (Instance Health)

1. Click **Add Widget → Metric Chart**.
2. Namespace:

   * `oci_computeagent`
3. Metric Name:

   * `CpuUtilization` or `DiskBytesRead`
4. Change **Chart Type** → `Status` if available.

This chart shows if the instance is reachable and healthy.

Alternative:

* Use a widget showing the instance **Lifecycle State** if available.

---

## 4. Hands-On Task 2 — Add Alarm Widgets

#### Purpose

Surface current alarms directly on the dashboard.

This helps real SREs quickly detect outages.

### Steps:

1. Click **Add Widget → Alarm**.
2. Choose your previously created CPU alarm:

   * `<student-id>-cpu-alarm`
3. Set display mode:

   * `Summary` or `Detailed`
4. Click **Add**.

Repeat if you create additional alarms (latency, uptime, etc.).

---

## 5. What You Should See on Your Dashboard:

* **BharatMart API Latency panel** (`api_latency_seconds` or `http_request_duration_seconds`)
* **BharatMart Error Rate panel** (`http_requests_total` filtered for errors)
* **Infrastructure metrics panel** (CPU Utilization, NetworkBytesIn/Out - complementary view)
* **Uptime panel** (instance health or status)
* **Alarm widget** showing OK/FIRING state

The dashboard now acts as a basic SRE observability console.

---

## 6. Summary of the Hands-On

Today you built:

* A custom SRE dashboard
* Latency visualization using BharatMart custom metrics (`api_latency_seconds` for latency)
* Error rate visualization using BharatMart metrics (`http_requests_total`)
* Infrastructure metrics (CPU, Network) as complementary panels
* Uptime and instance health visualization
* Alarm widgets for operational awareness

These are the foundations of an end-to-end observability system.

---

## 7. Solutions Key (Instructor Reference)

Use this to verify student dashboards.

### ✔ Solution Key — Task 1: Latency & Uptime Dashboard

#### Expected Widgets:

1. **BharatMart API Latency** (`api_latency_seconds` or `http_request_duration_seconds`)
2. **BharatMart Error Rate** (`http_requests_total` filtered for errors)
3. **Infrastructure Metrics** (CPU Utilization, NetworkBytesIn/Out - complementary)
4. **Instance Health / Status Panel**

#### Expected Dashboard Name:

```
<student-id>-sre-dashboard
```

#### Why These Panels Are Correct:

* **BharatMart custom metrics** (`api_latency_seconds`) show actual user-facing latency
* **Error rate from application metrics** (`http_requests_total`) shows real API errors
* **Infrastructure metrics** (CPU, Network) complement application metrics by showing resource usage
* **Uptime panel** shows instance availability

SRE dashboards must highlight **user-facing performance** using application-level custom metrics complemented by infrastructure metrics for complete observability.

### ✔ Solution Key — Task 2: Alarm Widgets

#### Expected Alarm Widget:

* `<student-id>-cpu-alarm`

#### Expected State:

* **OK** (normal) OR
* **FIRING** (if CPU exceeded threshold)

#### Why This Matters:

Alarms on dashboards give:

* Real-time visibility
* Quick triage paths
* Immediate understanding of system health

If students see real values updating, their dashboard is functioning correctly.

---

## End of Hands-On Document

