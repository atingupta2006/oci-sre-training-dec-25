# Day 2: Defining and Implementing SLOs/SLIs for Cloud-Native Services

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

#### Available Metrics for SLI/SLO Definition
* OCI infrastructure metrics (CPU, memory, network, disk from Compute instances)
* Load Balancer metrics (backend health, latency, request counts, error rates)
* BharatMart application metrics (HTTP latency, error counts, business metrics from `/metrics` endpoint)

This deployment setup ensures that all metrics discussed in this topic are available for SLI/SLO definition and monitoring.

---

## 1. Concept Overview

Designing effective **Service Level Indicators (SLIs)** and **Service Level Objectives (SLOs)** is foundational to measurable reliability engineering.

SLIs and SLOs translate production behaviour into measurable engineering signals. Instead of subjective opinions like "the system feels slow," SLIs and SLOs provide quantitative reliability definitions.

---

## 2. How This Applies to IT Engineers and Developers

#### IT Engineers

* Must ensure metrics are emitted, collected, and usable in Monitoring.
* Design network, compute, and infrastructure paths that produce SLI-aligned signals.
* Know how failures in networking or compute show up as SLI violations.

#### Developers

* Must write code that generates traceable, measurable behaviour.
* Implement structured logging, error codes, latency measurement, and request correlation.
* Validate reliability-impacting code paths before releasing.

#### Unified View

```
SLI = What to measure
SLO = Target for that measurement
Infrastructure & code must produce measurable signals
```

---

## 3. Key Principles

#### Principle 1: SLIs Should Measure User Experience

SLIs are **quantitative measurements** of system behaviour. Examples:

* Latency of API responses
* Success rate of requests
* Percentage of valid responses
* Availability of service endpoints

#### Principle 2: SLOs Should Be Realistic

SLOs should be:

* Based on historical performance
* Achievable with the current architecture
* Tied to business impact

#### Principle 3: Only Few SLIs Should Be Chosen

Over-monitoring creates noise; under-monitoring hides problems.

#### Principle 4: Measure At the Right Location

Measure the user-facing point, not internal components.

Example:

```
Correct SLI: Latency measured at LB → end user perspective
Incorrect SLI: DB query time only → internal metric
```

#### Principle 5: Tie SLOs to Error Budgets

Error budgets guide release decisions.

---

## 4. Real-World Example: API Latency SLI for BharatMart

**Scenario:** Measuring latency for BharatMart order API.

* **User-facing latency:** Measured at OCI Load Balancer level (end-to-end user experience)
* **Internal latency:** Developers collect latency from API code using metrics
* **SRE approach:** Uses Load Balancer latency for SLI, internal metrics from `/metrics` endpoint for debugging
* **Why it matters:** Order placement is revenue-critical; latency directly impacts user experience and conversions

---

## 5. Observing SLIs in BharatMart Platform

#### Available Metrics for SLI Definition

BharatMart exposes metrics at the `/metrics` endpoint that can be used to define SLIs:

##### Availability SLI

- Metric: `http_requests_total` with status_code labels
- Measure: Percentage of requests with 2xx/3xx status codes
- Access: `curl http://localhost:3000/metrics | grep http_requests_total`

##### Latency SLI

- Metric: `http_request_duration_seconds` histogram
- Measure: P95, P99 latencies from histogram buckets
- Access: `curl http://localhost:3000/metrics | grep http_request_duration_seconds`

##### Error Rate SLI

- Metric: `http_requests_total{status_code=~"5.."}` 
- Measure: Percentage of 5xx errors
- Access: Check metrics endpoint for error counts

##### Health SLI
- Endpoint: `/api/health`
- Measure: Availability based on health check responses
- Access: `curl http://localhost:3000/api/health`

---

## 6. Key Takeaways

* The `/metrics` endpoint provides all the data needed to measure SLIs
* Health check endpoint (`/api/health`) is essential for availability SLIs
* These metrics are automatically collected - no manual instrumentation needed
* Metrics follow Prometheus format, standard for SRE monitoring
* SLIs should measure user experience, not just internal metrics

