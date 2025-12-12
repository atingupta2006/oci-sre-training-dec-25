# **Day 5 – Automating Incident Archival with OCI Service Connector Hub**

### **Audience**

Cloud Engineers, DevOps Engineers, Observability Teams, and SREs.

### **Purpose**

This lab teaches you how to automatically capture and archive Monitoring alarm events using **OCI Service Connector Hub (SCH)** and **Object Storage**.

This provides a foundational building block for:

* Incident review
* Audit compliance
* Trends and analytics
* Multi-system integration
* Automated operational workflows

The focus is to understand *how Monitoring events move through OCI* and *how SCH can transform or redirect these events*.

---

# **0. Concepts Before You Begin**

To keep the lab simple but meaningful, here are the only key concepts you need.

---

## **0.1 What is a Monitoring Alarm Event?**

When a metric crosses its threshold, OCI Monitoring produces:

* The current metric details
* The alarm state transition (OK → FIRING → OK)
* The resource dimensions (e.g., instanceId)
* Severity information
* Timestamp

By default, OCI only shows the current alarm state, not a history.
This lab creates that history.

---

## **0.2 What is Service Connector Hub (SCH)?**

SCH is a **data movement automation service** that connects OCI services together.

Think of SCH as a **pipeline builder** for cloud events.

You define:

* **Source**: where the data comes from
* **Operator (optional)**: filter/transform
* **Target**: where the data goes

In our scenario:

* **Source = Monitoring**
* **Target = Object Storage**

SCH handles the flow automatically and reliably.

---

## **0.3 Why Use Object Storage as Target?**

Object Storage is:

* Durable
* Cheap
* Versioned
* Regional
* Easy to integrate with external tools

It’s the best location for archiving incident data long-term.

---

# **1. Architecture for This Lab**

The architecture is intentionally simple:

```
Monitoring → Service Connector Hub → Object Storage
```

### Flow Explanation:

1. You create one or more Monitoring alarms.
2. When these alarms fire or transition state, Monitoring generates event data.
3. SCH listens to Monitoring signals in the specified compartment.
4. SCH pushes the structured JSON event into an Object Storage bucket.
5. Each event becomes a separate object, creating a **timeline of alarms**.

This design requires **no code**, **no runtime**, and **no maintenance overhead**.

---

# **2. Prerequisites**

* Valid OCI tenancy
* Compartment with permissions to create alarms, SCH, and buckets
* At least one compute instance (to generate CPU metrics)
* Oracle Console access

Everything is done through the OCI Console—no CLI, Docker, or Functions.

---

# **3. Step 1 — Create the Object Storage Bucket**

1. Navigate to:
   **Storage → Object Storage → Buckets**
2. Select the correct compartment.
3. Click **Create Bucket**.
4. Enter:

   * **Name:** `incident-events-archive`
   * **Tier:** Standard
5. Leave other settings as default.
6. Click **Create**.

### 💡 Why this step matters

The bucket acts as a centralized archive of all alarm events.
Every event becomes a timestamped JSON file.

---

# **4. Step 2 — Create the Service Connector**

This step defines *how* Monitoring events will be routed into the bucket.

1. Go to:
   **Application Integration → Service Connector Hub**
2. Click **Create Connector**.

---

## **4.1 Basic Information**

* **Connector Name:** `incident-archival-connector`
* **Compartment:** Your lab compartment

---

## **4.2 Source: Monitoring**

* **Source Type:** Monitoring
* **Compartment:** your alarms’ compartment
* **Namespace Filter:** *Leave empty*
* **Dimension Filter:** *Leave empty*

### ✔ Why leave it empty?

Because empty filters mean:

* All namespaces
* All metrics
* All alarms

This ensures your connector captures *everything Monitoring emits* for the compartment.

This is especially helpful for:

* Demo environments
* Shared services
* Environments where alarms evolve over time
* Large teams who don’t want to adjust SCH each time a new alarm is added

---

## **4.3 Target: Object Storage**

* **Target Type:** Object Storage
* **Bucket:** `incident-events-archive`
* **Prefix:** `alarms/`

### ✔ Why use a prefix?

This organizes the archive like a folder structure:

```
incident-events-archive/
   alarms/
      alarm_event_2025_12_11_10_23_11.json
      alarm_event_2025_12_11_10_24_50.json
      ...
```

This makes it easier to query or integrate later.

---

## **4.4 Finish the Connector**

Click **Create**.

SCH will initialize and change to **Active** shortly.

### 💡 Behind the scenes

OCI automatically applies required IAM permissions for SCH to write to the bucket.
No manual IAM work is needed for this lab.

---

# **5. Step 3 — Create a Test Alarm**

This alarm fires quickly and provides real test data.

1. Navigate to:
   **Observability & Management → Monitoring → Alarms → Create Alarm**

2. Enter:

### **Alarm Details**

* **Name:** `cpu-test-alarm`
* **Compartment:** same as SCH source

### **Alarm Rule**

* Namespace: `oci_computeagent`
* Metric: `CpuUtilization`
* Statistic: Mean
* Operator: Greater than
* Threshold: `1`
* Trigger Delay: `1 minute`

### **Severity**

* Critical

3. Click **Create Alarm**.

The alarm will fire because CPU metrics almost always cross 1%.

---

# **6. Step 4 — Validate the Pipeline**

---

## **6.1 Check the alarm state**

1. Open the alarm.
2. Status should be: **FIRING**.

### Why?

This confirms Monitoring has generated an event, providing input to SCH.

---

## **6.2 Check the Service Connector**

1. Open:
   **Service Connector Hub → incident-archival-connector**
2. Go to the **Metrics** tab.
3. Verify:

   * "Events Processed" is increasing.

This confirms SCH is collecting Monitoring events.

---

## **6.3 Check Object Storage**

1. Navigate to:
   **Object Storage → incident-events-archive → alarms/**
2. You should see files like:

```
alarm_event_2025-12-11T12-04-49Z.json
```

3. Open one.

A typical alarm event looks like:

```json
{
  "alarmId": "ocid1.alarm.oc1..xxxx",
  "currentState": "FIRING",
  "previousState": "OK",
  "metricName": "CpuUtilization",
  "severity": "CRITICAL",
  "timestamp": "2025-12-11T12:04:49Z",
  "dimensions": {
    "instanceId": "ocid1.instance.oc1..abcd"
  }
}
```

### What this means

You have successfully created a **permanent, timestamped archive** of every alarm event.

---

# **7. Real-World Use Cases**

This workflow is not just a lab exercise — it is widely used in real operations.

---

## **Use Case 1 — Incident Investigation (Postmortem Analysis)**

Archived events allow SREs to reconstruct:

* When alarms fired
* How many times
* Which instances were affected
* Duration of impact

This is essential for RCA (Root Cause Analysis).

---

## **Use Case 2 — Compliance and Governance**

Many organizations must retain operational logs for **months or years**.
Object Storage is the cheapest and most durable option.

---

## **Use Case 3 — Machine Learning and Anomaly Detection**

Historical alarm data can feed:

* Trend detectors
* Predictive modeling
* Capacity planning tools

---

## **Use Case 4 — Multi-Region or Multi-Compartment Consolidation**

Use SCH in each compartment and send everything to a central bucket.
This creates a single source of truth for all alarms in the enterprise.

---

## **Use Case 5 — External Integrations (SIEM, Analytics Tools)**

Common workflows:

* Export bucket logs to **Splunk**
* Load into **ELK / OpenSearch**
* Import to **Snowflake**
* Feed into **Datadog** or **Grafana**

Object Storage is often the first location for external ingestion.

---

## **Use Case 6 — Billing / Cost Monitoring**

When alarms relate to billing metrics, keeping a historical log becomes essential for:

* Budget forecasting
* Usage anomaly detection
* Chargeback reports
