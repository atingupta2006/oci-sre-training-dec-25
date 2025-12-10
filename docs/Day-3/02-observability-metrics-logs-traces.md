# Day 3: Observability - Metrics, Logs, Traces

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** is already deployed on OCI with the following architecture:

#### Assumed Deployment
* **BharatMart API** running on one or more OCI Compute instances
* **OCI Load Balancer** distributing traffic to API instances
* **Database** (OCI Autonomous Database or Supabase) for data storage
* **OCI Cloud Agent** enabled on Compute instances for metric collection
* **BharatMart application** exposing Prometheus metrics at `/metrics` endpoint
* **Application logs** being generated (Winston logger with JSON format)
* **Optional tracing** configured (OpenTelemetry with OTLP exporter if enabled)

#### Available Observability Data
* **Metrics:** OCI infrastructure metrics, Load Balancer metrics, BharatMart Prometheus metrics from `/metrics` endpoint
* **Logs:** Application logs (API requests, errors, business events), system logs from Compute instances
* **Traces:** Distributed request tracing (if OpenTelemetry is configured and enabled)

---

## 1. Concept Overview

Observability is the ability to understand the internal state of a system **based on the data it produces**, especially during failures.
It goes beyond traditional monitoring by enabling engineers to:

* Ask new, unknown questions,
* Diagnose complex issues,
* Correlate signals across systems,
* Understand *why* something is happening, not just *what*.

Observability relies on **three pillars**:

1. **Metrics** – numerical measurements representing system behaviour.
2. **Logs** – event records providing detailed context.
3. **Traces** – request-level journey mapping across services.

While monitoring answers "is the system working?", observability answers "why is it behaving this way?".

---

## 2. How This Applies to IT Engineers and Developers

### IT Engineers

* Diagnose resource saturation.
* Correlate compute, network, and storage behaviours.
* Use metrics + logs + traces to identify bottlenecks.

### Developers

* Trace application-level requests.
* Inspect error logs and debug execution paths.
* Understand performance characteristics across microservices.

### Unified View

```
Metrics → What is happening?
Logs    → What events occurred?
Traces  → How did the request flow through systems?
```

Together → Full Observability.

---

## 3. Observability vs Monitoring

| Aspect   | Monitoring                | Observability             |
| -------- | ------------------------- | ------------------------- |
| Purpose  | Detect known issues       | Explore unknown issues    |
| Signals  | Mostly metrics            | Metrics, logs, traces     |
| Approach | Threshold-based           | Root-cause oriented       |
| Usage    | Alerts & surface symptoms | Diagnosis & deep analysis |

### Example:

* Monitoring alerts that CPU > 90%.
* Observability helps identify **which request**, **which code**, **which path** caused CPU spike.

---

## 4. The Three Pillars in Detail

### 4.1 Metrics

Numerical values representing system performance.
Examples:

* CPUUtilization
* MemoryUtilization
* Response latency
* Error counts

Key properties:

* Fast to query
* Useful for alerting
* Good for long-term trends

### 4.2 Logs

Detailed event records from systems and applications.
Examples:

* Application exceptions
* HTTP access logs
* System logs
* Security logs

Logs provide:

* Context around failures
* Precise timestamps
* Debugging information

### 4.3 Traces

Represent the journey of a request across services.
Useful for:

* Distributed systems
* Microservices architectures

Traces reveal:

* Slow components
* Internal dependencies
* Cross-service latency

---

## 5. Real-World Examples

### Example 1 — BharatMart Slow API Response

#### Scenario

Order placement latency spikes during peak shopping hours.

* **Metrics** from BharatMart `/metrics` endpoint show latency spike (P99 > 500ms).
* **Logs** from application logs show database connection timeouts.
* **Traces** reveal slow downstream dependency calls to payment gateway or database.
* **Correlation:** All three signals together identify root cause during incident investigation.

### Example 2 — BharatMart API CPU Saturation on OCI Compute

#### Scenario

BharatMart API instances experiencing high CPU during traffic spikes.

* **Metric** from OCI Monitoring identifies high CPU utilization (>85%) on Compute instances.
* **Logs** from BharatMart application logs show inefficient loop in order processing code.
* **Trace** shows high load concentrated on `/api/orders` endpoint during peak hours.
* **Action:** SRE team uses all three signals to prioritize optimization efforts.

### Example 3 — BharatMart Payment Gateway Failures

#### Scenario

External payment gateway experiencing intermittent failures.

* **Logs** from BharatMart show recurring 502 errors when calling payment API.
* **Metrics** from `/metrics` endpoint show increase in 5xx error count for payment-related routes.
* **Traces** pinpoint retry storms causing cascading failures and increased latency.
* **Resolution:** SRE team implements circuit breaker pattern using observability insights.

---

## 6. Best Practices

* Emit structured JSON logs.
* Use consistent tagging across metrics and logs.
* Enable Cloud Agent for full system telemetry.
* Use percentiles for latency tracking.
* Implement correlation IDs in logs and traces.

---

## 7. Common Mistakes

* Only relying on metrics without logs.
* Not enabling detailed logs for applications.
* Missing correlation identifiers.
* Using average metrics for decisions.

---

## 8. Additional Notes

* Observability investments pay off during high-severity incidents.
* This topic prepares you for logging-based metrics (next topic).
* Three pillars work together for complete system understanding.

