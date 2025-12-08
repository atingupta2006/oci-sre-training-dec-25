# Day 1: What is Site Reliability Engineering?

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** will be used throughout the training to demonstrate SRE concepts and OCI integration.

**Assumed Context:**

* **BharatMart platform** will be deployed on OCI for hands-on exercises
* **OCI resources** will be provisioned as needed for demonstrations and labs
* **Observability** features are built into BharatMart (metrics, logs, health endpoints)
* **SLIs and SLOs** will be defined using BharatMart metrics

#### Available for Practice
* BharatMart application exposing metrics at `/metrics` endpoint
* Health check endpoint at `/api/health`
* Structured JSON logs available for analysis
* OCI services for deployment, monitoring, and management

This context enables practical exercises in SRE fundamentals using a real application running on OCI.

---

## 1. Concept Overview

Site Reliability Engineering (SRE) is an engineering discipline focused on ensuring that systems run reliably, predictably, and at scale. It brings together principles from software engineering and infrastructure operations to remove uncertainty from production environments.

For IT engineers and developers, SRE can be summarized as:

* A way to engineer system reliability, rather than "manage" it.
* A structured approach to measure, improve, and automate system behaviour.
* A discipline that ensures the code you write or deploy behaves correctly under real workloads.
* A method to understand how applications behave under stress, failure, and unpredictable user patterns.

SRE is not a support function. It is an engineering role focused on system design, measurement, automation, and operational excellence.

### Conceptual Representation

```
Software Engineering + Systems Engineering + Operations Automation
                           |
                           v
                   Site Reliability Engineering
```

---

## 2. How This Applies to IT Engineers and Developers

#### For IT Engineers

* SRE provides structured tools and practices to reduce repetitive operational tasks.
* It clarifies how availability, latency, monitoring, and scaling should be engineered.
* Helps shift from:

  * Manual deployments → Automated CI/CD
  * Reactive troubleshooting → Proactive observability
  * Ad-hoc scripts → Standardised automation
  * Ticket-driven work → Measurable engineering improvements

#### For Developers

* SRE helps developers understand how their code behaves in real-world conditions.
* Ensures that the application is:

  * Observable
  * Measurable
  * Fault-tolerant
  * Scalable
* Helps answer:

  * What happens to my API when concurrency increases?
  * What happens when a downstream dependency slows?
  * What metrics prove that my feature is working correctly?

#### Developer ↔ IT Engineer ↔ SRE Relationship

```
Developer: Build the feature  
IT Engineer: Deploy and support the environment  
SRE: Ensure the entire system meets reliability targets
```

---

## 3. Key Principles

#### Reliability Must Be Measured

SRE defines reliability through SLIs (metrics) and SLOs (targets), removing subjectivity.

#### Automate Repetitive Work

Manual operations increase error risk; automation ensures consistency.

#### Systems Must Be Observable

Logs, metrics, and traces allow engineers to understand behaviour, troubleshoot, and improve systems.

#### BharatMart Implementation

The platform implements all three pillars of observability:

```
BharatMart Application (Express.js API)
  |        \            \
  |         \            \
 Logs     Metrics       Traces
  |          |            |
  v          v            v
Winston  Prometheus  OpenTelemetry
  |         |            
  v         v            
logs/    /metrics     
api.log  endpoint     
```

#### Key Observability Features
- **Metrics:** Prometheus metrics exposed at `/metrics` endpoint
- **Metrics Middleware:** Automatic request tracking and latency measurement
- **Logging:** Structured JSON logging via Winston logger
- **Tracing:** Optional distributed tracing via OpenTelemetry

#### Design for Failure

Systems should continue functioning even when components degrade.

#### Controlled Change Management

SRE ensures safe rollouts using strategies such as canary deployments and feature flags.

#### Blameless Learning Culture

Learning from incidents without individual blame.

---

## 4. Real-World Examples

### Example 1 — API Latency Spikes in BharatMart

#### Scenario

A new checkout feature increases API execution time.

* **Developer's Perspective:** Sees a need to optimise code for better performance.
* **SRE's Perspective:** Sees a P99 latency breach impacting user experience and potential revenue loss.

#### How BharatMart Demonstrates This

The platform includes built-in latency monitoring through Prometheus metrics:

- Every API request is automatically tracked for duration
- Metrics are exposed at `/metrics` endpoint in Prometheus format
- Key metric: `http_request_duration_seconds` - tracks all request latencies

#### SRE Actions in BharatMart

1. **Track latency SLIs** - Access metrics endpoint: `curl http://localhost:3000/metrics`
2. **Visualise P95/P99 spikes** - Query Prometheus for percentile distributions
3. **Work with developers** - Share metrics data to identify slow code paths
4. **Monitor continuously** - Set up alerts when P99 exceeds threshold (e.g., > 500ms)

### Example 2 — OCI Compute Instance Degradation

#### Scenario

An OCI VM running BharatMart slows down and becomes temporarily unresponsive.

* **IT Engineer's Action:** Restarts the instance, but the issue reappears.
* **SRE's Investigation:** Uses observability to find root cause.

#### How BharatMart Demonstrates This

The platform generates comprehensive metrics that would help identify the issue:

1. **HTTP Request Metrics** - Detecting slow API responses
   - `http_requests_total{status_code="500"}` - Server errors
   - `http_request_duration_seconds` - Response time degradation

2. **Application Logs** - Structured JSON logs for debugging

   BharatMart generates structured JSON logs with rich context. Example log entry:

   ```json
   {
     "coldStart": false,
     "environment": "development",
     "eventType": "api_request",
     "level": "error",
     "message": "API Request",
     "method": "GET",
     "path": "/api/orders",
     "response_time_ms": 5000,
     "service": "sre-training-platform",
     "span_id": "6312faf92861776b",
     "status_code": 500,
     "timestamp": "2025-11-30 16:49:50",
     "trace_id": "087fdc86277e500e32990e3ba6f77966"
   }
   ```

   These logs include OpenTelemetry tracing fields (`trace_id`, `span_id`) for distributed tracing correlation and can be ingested into OCI Logging Service.

3. **Business Metrics** - Impact on user transactions
   - `orders_failed_total` - Failed orders due to system issues
   - `payments_processed_total{status="failed"}` - Payment failures

#### SRE Actions in BharatMart

1. **Review metrics** - Check `/metrics` endpoint for error rates and latency spikes
2. **Analyze logs** - Review `logs/api.log` for error patterns and stack traces
3. **Identify root cause** - Correlate metrics (high latency) with logs (database connection pool exhaustion)
4. **Implement monitoring** - Set up Prometheus alerts for error rate thresholds
5. **Document solution** - Create runbook for similar incidents

---

## 5. BharatMart Platform: SRE Principles in Practice

BharatMart is an e-commerce platform specifically designed for SRE training. It demonstrates SRE principles through:

### Measurability
- **Prometheus metrics** at `/metrics` endpoint
- Business metrics: orders, payments, inventory
- System metrics: HTTP requests, latency, errors

### Observability
- **Structured JSON logging** for easy parsing and analysis
- **Distributed tracing** via OpenTelemetry (optional)
- **Health endpoints** for automated monitoring

### Reliability Engineering
- **Chaos engineering** capabilities for resilience testing
- **Multiple deployment modes** (single-VM, multi-tier, OCI PaaS)
- **Adapter pattern** for infrastructure flexibility

### Automation
- **Background workers** for async processing
- **Infrastructure as Code** examples
- **Automated testing** suite included

Throughout this training, you'll use BharatMart to practice SRE concepts with a real, production-grade application.

