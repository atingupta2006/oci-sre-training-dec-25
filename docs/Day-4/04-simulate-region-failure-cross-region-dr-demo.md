# Day 4: Simulate Region Failure and Test Cross-Region DR - Demonstration

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

This is an instructor-led demonstration. Students observe cross-region disaster recovery testing.

**Assumed Context:**
* **BharatMart** deployed in multiple regions (primary and DR)
* **Cross-region replication** configured
* **Failover procedures** documented and tested

---

## 1. Purpose

Demonstrate how to test cross-region disaster recovery capabilities and validate that systems can recover from region-level failures.

---

## 2. Prerequisites

* BharatMart deployed in primary and secondary regions
* Cross-region data replication configured
* Failover procedures documented
* Monitoring configured across regions

---

## 3. What You'll Demonstrate

1. **Multi-Region Architecture**
   * Primary region setup
   * Secondary (DR) region setup
   * Data replication strategy

2. **Region Failure Simulation**
   * Simulate primary region failure
   * Test automatic or manual failover
   * Validate DR region activation

3. **Recovery Validation**
   * Verify service availability in DR region
   * Validate data consistency
   * Test failback procedures

---

## 4. Demonstration Steps

#### Step 1: Review Multi-Region Setup

1. Show primary region deployment:
   * Compute instances running BharatMart API
   * Database in primary region
   * Load Balancer serving traffic

2. Show secondary (DR) region:
   * Standby infrastructure
   * Database replication
   * Backup Load Balancer

---

#### Step 2: Simulate Primary Region Failure

1. **Method 1 - Network Isolation:**
   * Block traffic to primary region (simulated)
   * Show monitoring detects failure
   * Demonstrate failover trigger

2. **Method 2 - Service Shutdown:**
   * Stop primary region services (for demonstration)
   * Show health check failures
   * Observe automatic failover

---

#### Step 3: Observe Failover Process

1. **Monitor Failover:**
   * Show traffic routing to DR region
   * Verify DR region services active
   * Check data availability

2. **Validate Service Continuity:**
   * Test API endpoints in DR region
   * Verify database accessibility
   * Confirm user traffic handling

---

#### Step 4: Test Failback

1. **Restore Primary Region:**
   * Bring primary region back online
   * Sync data from DR to primary
   * Validate data consistency

2. **Failback Process:**
   * Gradually route traffic back to primary
   * Monitor for issues
   * Complete failback validation

---

## 5. Key Points to Emphasize

* **Disaster Recovery Planning:** Essential for critical services
* **Testing Regularly:** DR must be tested to ensure it works
* **Data Replication:** Critical for maintaining data consistency
* **Failover Speed:** RTO (Recovery Time Objective) matters
* **Data Loss Prevention:** RPO (Recovery Point Objective) considerations

---

## 6. What Students Should Observe

* Multi-region architecture design
* Failover mechanisms in action
* Recovery time and procedures
* Data consistency validation
* Importance of regular DR testing

---

## End of Demonstration Document

