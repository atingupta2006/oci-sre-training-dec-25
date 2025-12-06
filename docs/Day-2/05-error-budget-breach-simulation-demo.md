# Day 2: Error Budget Breach Simulation Using OCI Health Checks and Failover Testing (Demonstration)

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

This is an instructor-led demonstration. Students observe error budget breach scenarios and automatic failover.

**Assumed Context:**
* **BharatMart** deployed with Load Balancer and multiple backend instances
* **OCI Monitoring alarms** configured
* **Health checks** configured on `/api/health` endpoint

---

## 1. Purpose

Demonstrate how error budget breaches occur and how OCI health checks and failover mechanisms help protect against SLO violations.

---

## 2. Prerequisites

* BharatMart deployed with Load Balancer and multiple backend instances
* OCI Monitoring alarms configured
* Health checks configured on `/api/health` endpoint

---

## 3. What You'll Demonstrate

1. **Baseline Performance**
   * Current SLO compliance status
   * Normal error rate and latency
   * Healthy backend instances

2. **Simulate Failure Scenario**
   * Stop one backend instance (simulating failure)
   * Inject errors (simulating bug or overload)
   * Monitor error budget consumption

3. **Observe Automatic Response**
   * Health check failure detection
   * Load Balancer failover to healthy backends
   * Automatic traffic rerouting

4. **Monitor Error Budget Impact**
   * Track error rate increase
   * Calculate error budget burn rate
   * Observe alarm triggers

---

## 4. Demonstration Steps

#### Step 1: Establish Baseline

1. **Review Current Metrics:**
   - Access **OCI Console** → **Monitoring** → **Metric Explorer**
   - Check current error rate (should be < 0.5%)
   - Verify all backend instances healthy
   - Review P99 latency (should be < 500ms)

2. **Check Error Budget Status:**
   - Calculate current month's error count
   - Display error budget remaining (e.g., 8,500 / 10,000 remaining)

#### Step 2: Simulate Backend Failure

1. **Stop One Backend Instance:**
   ```bash
   # SSH to one backend instance
   sudo systemctl stop bharatmart-api
   ```

2. **Observe Health Check Response:**
   - Health check on `/api/health` starts failing
   - Load Balancer marks backend as unhealthy
   - Traffic automatically routes to remaining healthy backends

3. **Monitor in OCI Console:**
   - **Load Balancer** → **Backend Sets** → Check unhealthy backend count
   - **Monitoring** → **Metric Explorer** → Check `BackendHealthyHostCount`

#### Step 3: Inject Errors (Simulate Bug)

1. **Enable Chaos Engineering:**
   - Set environment variable: `CHAOS_ENABLED=true`
   - Configure error rate: `CHAOS_ERROR_RATE=0.1` (10% errors)

2. **Monitor Error Rate Increase:**
   - Access **Metric Explorer**
   - Query: `http_requests_total{status_code="500"}`
   - Observe error rate climbing

3. **Track Error Budget Consumption:**
   - Calculate: Errors per minute × minutes remaining in month
   - Display burn rate projection
   - Show error budget depletion timeline

#### Step 4: Observe Automatic Mitigation

1. **Health Check Recovery:**
   - If backend recovers, health checks pass
   - Load Balancer automatically adds backend back to pool

2. **Error Rate Normalization:**
   - Once chaos disabled, error rate returns to baseline
   - Error budget burn stops (unless already exhausted)

3. **Alarm Triggers:**
   - Review triggered alarms in **Monitoring** → **Alarms**
   - Check notification delivery (email/SMS)
   - Review alarm state changes

#### Step 5: Analyze Error Budget Impact

1. **Calculate Consumption:**
   ```
   Errors during simulation: 500 errors
   Error budget consumed: 500 / 10,000 = 5%
   Remaining budget: 8,000 / 10,000 = 80%
   ```

2. **Policy Implications:**
   - If < 50% consumed: Continue normal operations
   - If 50-75% consumed: Warning, slow feature velocity
   - If > 75% consumed: Pause releases, focus on stability

---

## 5. Key Points to Emphasize

* **Automatic Failover:** OCI Load Balancer handles backend failures automatically
* **Health Checks:** Essential for availability SLI measurement
* **Error Budget Visibility:** Real-time tracking enables proactive decisions
* **Policy Enforcement:** Clear thresholds guide release decisions

---

## 6. What Students Should Observe

* How failures impact error budget
* Automatic failover mechanisms
* Error budget burn rate calculation
* Policy enforcement based on error budget status

