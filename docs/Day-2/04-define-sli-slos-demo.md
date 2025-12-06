# Day 2: Define SLI/SLOs for a Sample Web App Running on OCI Load Balancer + Compute (Demonstration)

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

This is an instructor-led demonstration. Students observe the SLI/SLO definition process.

**Assumed Context:**
* **BharatMart** deployed on OCI with Load Balancer
* **OCI Monitoring** access available
* **Metrics** available from both Load Balancer and application

---

## 1. Purpose

Demonstrate how to define meaningful SLIs and SLOs for BharatMart application running on OCI, using both infrastructure metrics and application metrics.

---

## 2. Prerequisites

* BharatMart deployed on OCI with Load Balancer
* OCI Monitoring access
* Metrics available from both Load Balancer and application

---

## 3. What You'll Demonstrate

1. **Identify Critical User Journeys**
   * Order placement flow
   * Product browsing flow
   * Payment processing flow

2. **Select Appropriate Metrics**
   * Load Balancer latency for user-facing experience
   * Application error rates from `/metrics` endpoint
   * Infrastructure health metrics

3. **Define SLIs**
   * Availability SLI
   * Latency SLI
   * Error Rate SLI

4. **Set SLO Targets**
   * Based on historical performance
   * Aligned with business requirements
   * Achievable with current architecture

5. **Calculate Error Budgets**
   * Based on SLO targets
   * Monthly traffic estimates
   * Policy thresholds

---

## 4. Demonstration Steps

#### Step 1: Review Current Metrics

1. Access **OCI Console** → **Observability & Management** → **Monitoring** → **Metric Explorer**
2. Review available metrics:
   - **OCI Load Balancer:** `BackendResponseTime`, `HttpResponseCounts`
   - **OCI Compute:** `CpuUtilization`, `MemoryUtilization`
   - **BharatMart Application:** (if custom metrics configured) `http_request_duration_seconds`, `http_requests_total`

3. Access BharatMart metrics endpoint:
   ```bash
   curl http://<load-balancer-ip>/metrics
   ```
   Review available Prometheus metrics

#### Step 2: Define Availability SLI

1. **SLI Definition:**
   ```
   SLI: Percentage of successful HTTP requests (2xx/3xx status codes)
   Measurement: From Load Balancer HttpResponseCounts or BharatMart http_requests_total
   ```

2. **Query in Metric Explorer:**
   - Namespace: `oci_lbaas` or `custom.bharatmart`
   - Metric: `HttpResponseCounts` or `http_requests_total`
   - Filter: `status_code = 2xx or 3xx`
   - Calculate: `(successful_requests / total_requests) * 100`

3. **Set SLO:**
   ```
   SLO: 99.5% availability over 30-day window
   ```

#### Step 3: Define Latency SLI

1. **SLI Definition:**
   ```
   SLI: P99 latency for order API requests
   Measurement: From Load Balancer BackendResponseTime or BharatMart http_request_duration_seconds
   ```

2. **Query in Metric Explorer:**
   - Namespace: `oci_lbaas` or `custom.bharatmart`
   - Metric: `BackendResponseTime` or `http_request_duration_seconds`
   - Statistic: `P99`
   - Filter: `route = "/api/orders"` (if applicable)

3. **Set SLO:**
   ```
   SLO: P99 latency < 500ms for order API
   ```

#### Step 4: Define Error Rate SLI

1. **SLI Definition:**
   ```
   SLI: Percentage of 5xx errors
   Measurement: From Load Balancer or BharatMart metrics
   ```

2. **Query in Metric Explorer:**
   - Filter: `status_code = 5xx`
   - Calculate error rate: `(5xx_errors / total_requests) * 100`

3. **Set SLO:**
   ```
   SLO: Error rate < 0.5% (aligned with 99.5% availability SLO)
   ```

#### Step 5: Calculate Error Budget

1. **Assumptions:**
   - Monthly traffic: 2,000,000 requests
   - Availability SLO: 99.5%

2. **Calculation:**
   ```
   Allowed failures = 0.5% of 2,000,000 = 10,000 failures/month
   ```

3. **Policy Thresholds:**
   - **Warning (50%):** 5,000 failures → Slow feature velocity
   - **Critical (75%):** 7,500 failures → Pause releases
   - **Exhausted (100%):** 10,000 failures → Full freeze

---

## 5. Key Points to Emphasize

* **User-Facing Focus:** SLIs should measure what users experience
* **Multiple Data Sources:** Combine Load Balancer and application metrics
* **Realistic Targets:** SLOs based on historical performance, not aspirations
* **Business Alignment:** Error budgets tied to business impact

---

## 6. What Students Should Observe

* How to identify critical user journeys
* Metric selection for SLI definition
* SLO target setting process
* Error budget calculation methodology

