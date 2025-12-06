# Day 3: The Role of Automation in SRE and Types of Automation

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** is deployed on OCI and uses automation to reduce toil.

**Assumed Context:**
* **BharatMart** deployed on OCI with automated infrastructure provisioning
* **OCI services** (Resource Manager, Functions, Events, Auto Scaling) available for automation
* **Automation** reduces manual operational tasks

---

## 1. Concept Overview

Automation is a core principle of SRE, serving as the primary mechanism for eliminating toil and improving reliability. Effective automation allows SRE teams to:

* Focus engineering effort on valuable work rather than repetitive tasks
* Ensure consistent, error-free operations
* Scale operations without proportional increases in team size
* Improve system reliability through predictable, repeatable processes

---

## 2. How Automation Fits into SRE

### Why Automation Matters

* **Eliminates Toil:** Reduces manual, repetitive work
* **Reduces Errors:** Automated processes are more consistent than manual operations
* **Enables Scale:** Systems can grow without proportional operational overhead
* **Improves Reliability:** Predictable, repeatable operations reduce failures
* **Frees Engineering Time:** Team can focus on building and improving systems

### Automation vs Manual Work

```
Manual Operations → High Error Rate → Slow → High Toil
Automated Operations → Low Error Rate → Fast → Low Toil
```

---

## 3. Types of Automation in SRE

### 3.1 Infrastructure Automation

**Purpose:** Automate provisioning, configuration, and management of infrastructure.

**Examples:**
* Infrastructure as Code (Terraform, OCI Resource Manager)
* Automated deployment pipelines
* Configuration management

**BharatMart Example:**
* Terraform templates for OCI infrastructure (VCN, Compute, Load Balancer)
* OCI Resource Manager for managed Terraform execution
* Consistent deployments across environments

---

### 3.2 Operational Automation

**Purpose:** Automate routine operational tasks and responses.

**Examples:**
* Automated health checks and restarts
* Auto-scaling based on metrics
* Automated backups and snapshots
* Scheduled maintenance tasks

**BharatMart Example:**
* OCI Auto Scaling for Compute instances
* Health checks on Load Balancer with automatic failover
* Scheduled Functions for routine maintenance

---

### 3.3 Monitoring and Alerting Automation

**Purpose:** Automate detection, analysis, and response to issues.

**Examples:**
* Automated metric collection
* Log-based metric extraction
* Automated alerting and notifications
* Self-healing systems

**BharatMart Example:**
* OCI Monitoring with custom metrics from `/metrics` endpoint
* Log-based metrics from application logs
* Automated alarms on SLO violations

---

### 3.4 Incident Response Automation

**Purpose:** Automate parts of incident detection and response.

**Examples:**
* Runbook automation
* Automated rollbacks
* Circuit breakers and retry logic
* Automated failover

**BharatMart Example:**
* Automated traffic failover via Load Balancer health checks
* Circuit breaker patterns in application code
* Automated rollback via CI/CD pipelines

---

### 3.5 Testing and Validation Automation

**Purpose:** Automate testing and validation of systems.

**Examples:**
* Automated testing pipelines
* Chaos engineering experiments
* Performance testing
* Compliance checks

**BharatMart Example:**
* Automated E2E tests
* Chaos engineering features for resilience testing
* Performance testing in CI/CD

---

## 4. Automation Patterns

### 4.1 Infrastructure as Code (IaC)

**Pattern:** Define infrastructure in code, version control it, and provision automatically.

**Tools:** Terraform, OCI Resource Manager

**Benefit:** Repeatable, consistent infrastructure deployments

---

### 4.2 Event-Driven Automation

**Pattern:** Automate responses to events and triggers.

**Tools:** OCI Functions, OCI Events

**Benefit:** Reactive automation that responds to system events

---

### 4.3 Scheduled Automation

**Pattern:** Automate tasks that run on a schedule.

**Tools:** OCI Functions with Events, Cron jobs

**Benefit:** Routine tasks handled automatically without manual intervention

---

### 4.4 Self-Healing Systems

**Pattern:** Systems automatically detect and recover from failures.

**Tools:** Health checks, auto-scaling, circuit breakers

**Benefit:** Reduced downtime and manual intervention

---

## 5. Real-World Examples

### Example 1 — Automated Infrastructure Provisioning

**Scenario:** Provisioning BharatMart infrastructure manually takes 4 hours and is error-prone.

**Automation Solution:**
* Terraform templates define all infrastructure
* OCI Resource Manager executes Terraform automatically
* Infrastructure provisioned in 15 minutes with zero errors

**Impact:** 95% reduction in provisioning time, elimination of configuration errors

---

### Example 2 — Automated Scaling

**Scenario:** Manual instance scaling during peak traffic takes 30 minutes and causes performance degradation.

**Automation Solution:**
* OCI Auto Scaling configured based on CPU utilization
* Instances scale automatically when CPU > 70%
* Scaling completes in 2-3 minutes

**Impact:** No performance degradation during traffic spikes, zero manual intervention

---

### Example 3 — Automated Log Monitoring

**Scenario:** Engineers manually check logs for errors multiple times per day.

**Automation Solution:**
* Log-based metrics extract error counts from application logs
* OCI alarms trigger when error rate exceeds threshold
* Notifications sent to on-call engineer automatically

**Impact:** Proactive error detection, elimination of manual log checking

---

## 6. Automation Best Practices

* **Start Small:** Automate high-toil tasks first
* **Version Control:** Store automation code in version control
* **Test Automation:** Test automation code like application code
* **Monitor Automation:** Monitor automation itself for failures
* **Documentation:** Document automation and its purpose
* **Incremental:** Automate incrementally rather than all at once
* **Maintainability:** Design automation to be maintainable and debuggable

---

## 7. Common Mistakes

* Automating everything without prioritization
* Not testing automation thoroughly
* Creating automation that's hard to maintain
* Ignoring automation failures
* Not documenting automation
* Automating symptoms rather than root causes

---

## 8. OCI Services for Automation

### OCI Resource Manager
* Managed Terraform execution
* Infrastructure as Code automation

### OCI Functions
* Serverless function execution
* Event-driven automation

### OCI Events
* Event routing and triggers
* Scheduled automation

### OCI Auto Scaling
* Automatic instance scaling
* Self-healing infrastructure

### OCI Monitoring Alarms
* Automated alerting
* Metric-based automation triggers

---

## 9. Additional Notes

* Automation is an investment that pays dividends over time
* Balance automation effort with value gained
* Automation should reduce toil, not create new operational overhead
* This topic prepares you for hands-on automation labs

