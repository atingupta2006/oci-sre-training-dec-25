# Day 3: Create Logging Metrics, Push to OCI Monitoring, and Visualize - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will create logging-based metrics from BharatMart application logs.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* BharatMart logs ingested into OCI Logging Service (from previous lab)
* Access to OCI Console

---

## 1. Objective of This Hands-On

By the end of this exercise, students will:

* Understand logging-based metrics
* Build log queries in OCI Logging
* Convert log patterns into custom metrics
* Plot those metrics on an OCI dashboard
* Use log-derived metrics for monitoring and alerting

---

## 2. Background Concepts

### 2.1 What Are Logging-Based Metrics?

Logging-based metrics let you turn **log events** into **numeric measurements**.

Examples:

* Count of 5xx errors per minute
* Number of failed login attempts
* Order placement success count
* Slow request warnings

This is useful when:

* Your app logs contain reliability signals
* You need fine-grained insights from message patterns
* You want to track custom events without instrumenting code

### 2.2 Why Logging-Based Metrics Matter for SRE

They allow you to:

* Tie log patterns to SLO indicators
* Generate alerts from critical logs
* Visualize application behaviors
* Detect anomalies from log-based events

### 2.3 BharatMart Structured Logs

The BharatMart application uses **structured JSON logging** via Winston logger. Logs contain fields like:

* `timestamp`, `level`, `message`, `route`, `status_code`
* Business context: `orderId`, `userId`, `paymentStatus`

Example log entry:
```json
{"timestamp":"2025-11-14T12:01:05Z","level":"error","route":"/api/orders","status_code":500,"message":"Order creation failed","orderId":"123"}
```

This structured format makes it easy to create logging-based metrics using OCI Logging Query Language (LQL).

---

## 3. Hands-On Task 1 — Create a Logging Query

#### Purpose

Identify patterns in logs for generating metrics.

### Steps:

1. Open **Navigation Menu (☰) → Observability & Management → Logging**.
2. Click **Log Groups**.
3. Select your log group: `<student-id>-log-group`.
4. Open your application log: `<student-id>-bharatmart-api-log`.
5. Click **Search**.

### Create Queries:

#### Query 1: Count Failed Order Placements
```
level = 'error' and route = '/api/orders'
```

#### Query 2: Count Successful Order Placements
```
level = 'info' and message contains 'Order created'
```

#### Query 3: Count 5xx Errors
```
level = 'error' and status_code >= 500
```

#### Query 4: Count All Errors
```
level = 'error'
```

6. Run each query and verify results.
7. Validate that logs contain measurable activities.

### Expected Result:

* You see log entries that match the selected pattern
* You validate the logs contain measurable activities
* Query syntax is correct and returns results

---

## 4. Hands-On Task 2 — Create a Metric From Log Query

#### Purpose

Convert log patterns into a metric.

OCI can convert **any log query** into a **custom metric**.

### Steps:

1. With your log query active (e.g., `level = 'error' and route = '/api/orders'`), click **Save as Metric** or **Create Metric**.
2. Fill the details:

   * **Metric Name:** `<student-id>-order-failures` (or similar)
   * **Namespace:** `oci_logging` (default) or `custom.bharatmart`
   * **Unit:** `count`
   * **Interval:** `1m` (1 minute)
   * **Query:** (your log query, e.g., `level = 'error' and route = '/api/orders'`)
3. Click **Create** or **Save**.

OCI now emits a new metric **every minute** based on matching logs.

### Repeat for Additional Metrics:

Create metrics for:

* Error count: `level = 'error'`
* Order failures: `level = 'error' and route = '/api/orders'`
* Payment failures: `level = 'error' and route = '/api/payments'`

### Expected Result:

* Metric creation confirmation
* New metric available in Metric Explorer
* Metric updating every minute based on log entries

---

## 5. Hands-On Task 3 — Verify Metrics in Metric Explorer

#### Purpose

Verify that logging-based metrics are being generated.

### Steps:

1. Open **Navigation Menu → Observability & Management → Monitoring → Metric Explorer**.
2. Select namespace: `oci_logging` (or your custom namespace).
3. Select metric: `<student-id>-order-failures` (or your metric name).
4. View metric data:
   - Select time range (last 1 hour, last 24 hours, etc.)
   - View graph showing metric values over time
5. Verify metric is updating:
   - Generate some errors by making API requests:
     ```bash
     # Generate errors (if your app has error endpoints)
     curl http://localhost:3000/api/nonexistent
     ```
   - Wait 1-2 minutes
   - Refresh metric view
   - Verify metric values increased

### Expected Result:

* Metrics visible in Metric Explorer
* Metrics updating based on log entries
* Graph shows metric values over time

---

## 6. Hands-On Task 4 — Plot Metrics on Dashboard

#### Purpose

Visualize log-derived metrics on a dashboard.

### Steps:

1. Open **Observability & Management → Dashboards**.
2. Select your dashboard:
   * `<student-id>-sre-dashboard` (from Day 2) OR
   * Create new dashboard: `<student-id>-logging-metrics-dashboard`
3. Click **Add Widget → Metric Chart**.
4. Configure the chart:

   * **Namespace:** `oci_logging` (or your custom namespace)
   * **Metric Name:** `<student-id>-order-failures`
   * **Statistic:** `Sum` or `Count`
   * **Interval:** `1 minute`
5. Title the chart:
   * `Order Placement Failures Per Minute (from Logs)`
6. Click **Create**.

### Add Additional Widgets:

Repeat to add widgets for:

* Total error count
* Payment failures
* Successful orders (if you created that metric)

### Expected Result:

* Dashboard shows log-based metrics
* Charts updating in real-time
* Visual representation of log patterns
* Metrics complement application metrics for complete observability

---

## 7. Summary of the Hands-On

In this exercise, you:

* Created log queries to identify patterns
* Converted log patterns into custom metrics
* Verified metrics in Metric Explorer
* Added metrics to dashboards for visualization

This is critical for:

* Error budget tracking
* Detecting production anomalies
* Creating actionable alarms
* Complete observability using logs + metrics

---

## 8. Solutions Key (Instructor Reference)

### ✔ Solution Key — Task 1: Logging Query

#### Expected Working Queries:

* For failed order placements:
  ```
  level = 'error' and route = '/api/orders'
  ```
* For successful order placements:
  ```
  level = 'info' and message contains 'Order created'
  ```
* For errors:
  ```
  level = 'error'
  ```

If structured logs were added, these patterns appear frequently.

### ✔ Solution Key — Task 2: Metric Creation

#### Expected Configuration:

* Metric Name: `<student-id>-order-failures`
* Namespace: `oci_logging` or `custom.bharatmart`
* Interval: `1 minute`
* Unit: `count`
* Query: `level = 'error' and route = '/api/orders'`

#### Expected Outcome:

* Metric should appear in **Metric Explorer** within 2–3 minutes
* Metric values updating every minute based on log entries

### ✔ Solution Key — Task 3: Metric Verification

#### Expected Results:

* Metric visible in Metric Explorer
* Graph showing metric values over time
* Values updating when new log entries match query

### ✔ Solution Key — Task 4: Dashboard Plot

#### Expected Visualization:

* Title: "Order Placement Failures Per Minute (from Logs)"
* Namespace: `oci_logging`
* Metric Name: `<student-id>-order-failures`
* Statistic: `Sum` or `Count`
* Spikes only appear during failed order placement attempts
* Chart updating in real-time

---

## 9. Next Steps

* Create alarms based on log-derived metrics
* Combine log-based metrics with application metrics in dashboards
* Use log-based metrics for SLO tracking
* Create additional metrics for other log patterns

---

## End of Hands-On Document

