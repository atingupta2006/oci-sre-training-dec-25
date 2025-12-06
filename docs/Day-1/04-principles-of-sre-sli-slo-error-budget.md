# Day 1: Principles of SRE (SLI, SLO, Error Budget)

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** will be used to demonstrate SLI, SLO, and Error Budget concepts.

**Assumed Context:**

* **BharatMart platform** exposes metrics at `/metrics` endpoint
* **Metrics** are available for SLI definition
* **Health endpoints** (`/api/health`) available for availability SLIs

---

## 1. Concept Overview

This topic introduces **SLIs (Service Level Indicators)**, **SLOs (Service Level Objectives)**, and **Error Budgets**, which together form the foundational reliability measurement framework in SRE.

For IT engineers and developers, these concepts translate production behaviour into measurable engineering signals. Instead of subjective opinions like "the system feels slow," SLIs and SLOs provide quantitative reliability definitions. Error budgets govern **how much unreliability is tolerable** before releases must pause and stability work must take priority.

---

## 2. How This Applies to IT Engineers and Developers

#### IT Engineers

* SLIs help identify where reliability degrades across infrastructure.
* SLOs provide clear operational targets for uptime, latency, and error rates.
* Error budgets guide when changes are safe versus risky.

#### Developers

* SLOs define how fast APIs must respond and how many failures are acceptable.
* SLIs reveal how code changes impact user-visible reliability.
* Error budgets define whether new features can be released or need rollback.

#### Realistic Mapping

```
SLI → A metric reflecting actual user experience
SLO → The target the engineering team commits to
Error Budget → Allowable failure within that target
```

---

## 3. Key Principles

#### Principle 1: SLIs Reflect User Experience

SLIs are **quantitative measurements** of system behaviour. Examples:

* API success rate
* Request latency (P95 / P99)
* Throughput
* Availability
* Data freshness

#### Principle 2: SLOs Are Engineering Commitments

SLOs define a reliability target:

```
Example:
"99.9% successful API requests per 30-day window"
```

#### Principle 3: Error Budgets Balance Innovation and Stability

Error budgets quantify the **acceptable failure**, such as:

```
If SLO = 99.9% → allowable errors = 0.1% of requests
```

#### Principle 4: Decisions Are Data-Driven

SRE decisions are not emotional; they are based on SLO compliance.

---

## 4. Diagram: Relationship Overview

```
User Behaviour
     |
     v
SLIs (Measured Data)
     |
     v
SLOs (Targets)
     |
     v
Error Budget (Allowed Failure)
     |
     v
Engineering Decisions (Release / Stabilise)
```

---

## 5. Real-World Example: API Latency SLO in BharatMart

#### Scenario

API latency degrades during peak shopping hours.

#### How BharatMart Demonstrates This
* **SLI:** Request latency measured at 99th percentile from `/metrics` endpoint
* **Metrics Available:** `http_request_duration_seconds` histogram tracks all request latencies
* **SLO Target:** P99 latency < 500ms
* **Detection:** Monitoring metrics endpoint shows P99 latency climbing from 200ms to 1500ms
* **Action:** Developers identify slow database query; IT engineers validate scalability improvements on OCI Compute

#### Key Point

Metrics exposed at `/metrics` endpoint provide the data needed to measure SLIs and validate SLO compliance.

---

## 6. Observing SLIs in BharatMart Platform

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

## 7. Key Takeaways

* The `/metrics` endpoint provides all the data needed to measure SLIs
* Health check endpoint (`/api/health`) is essential for availability SLIs
* These metrics are automatically collected - no manual instrumentation needed
* Metrics follow Prometheus format, standard for SRE monitoring
* SLIs, SLOs, and Error Budgets provide the measurement framework for reliability

