# Day 4: Run Failure Injection Using OCI CLI and Chaos Simulation Scripts - Demonstration

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

This is an instructor-led demonstration. Students observe failure injection using chaos engineering.

**Assumed Context:**
* **BharatMart** deployed on OCI with monitoring
* **OCI CLI** configured and accessible
* **Chaos engineering** features available in application

---

## 1. Purpose

Demonstrate how to inject controlled failures to test system resilience and validate failover mechanisms.

---

## 2. Prerequisites

* BharatMart deployed with Load Balancer and multiple backends
* OCI CLI installed and configured
* Monitoring and alerting configured
* Chaos engineering enabled in application

---

## 3. What You'll Demonstrate

1. **Chaos Engineering Concepts**
   * Controlled failure injection
   * System behavior under stress
   * Resilience validation

2. **Failure Scenarios**
   * Instance failures
   * Latency injection
   * Error injection
   * Network issues

3. **Observing System Response**
   * Automatic failover
   * Monitoring and alerting
   * Recovery mechanisms

---

## 4. Demonstration Steps

#### Step 1: Baseline System State

1. **Check Current State:**
2. **Review Metrics:**
---

#### Step 2: Inject Instance Failure

1. **Stop One Backend Instance:**
   ```bash
   # Stop instance
   ```

2. **Observe System Response:**
   * Load Balancer detects failure
   * Traffic automatically rerouted
   * Health checks mark backend as unhealthy
   * Remaining backends handle traffic

3. **Monitor Metrics:**
   * Show latency spike during failover
   * Verify service continues operating
   * Confirm no errors for users

---

#### Step 3: Inject Latency (Chaos Engineering)

1. **Enable Chaos Engineering:**
   ```bash
   # SSH to instance
   ssh opc@<instance-ip>
   
   # Set chaos environment variable
   export CHAOS_ENABLED=true
   export CHAOS_LATENCY_MS=500
   
   # Restart application
   sudo systemctl restart bharatmart-api
   ```

2. **Observe Impact:**
   * Metrics show latency increase (P95 > 500ms)
   * Users experience slower responses
   * Alarms trigger if thresholds exceeded

3. **Monitor System Behavior:**
   * Check if auto-scaling triggers
   * Verify timeout and retry logic
   * Observe error handling

---
