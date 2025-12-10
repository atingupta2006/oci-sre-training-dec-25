# Day 3: What is Toil and Why It Must Be Reduced

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** is already deployed on OCI and running in production. The platform generates operational work that requires manual intervention, which is the focus of toil identification and reduction.

#### Assumed Deployment
* **BharatMart API** running on one or more OCI Compute instances
* **OCI Load Balancer** distributing traffic to API instances
* **Database** (OCI Autonomous Database or Supabase) for data storage
* Application logs, metrics, and alarms configured

#### How to Deploy

BharatMart infrastructure can be deployed using **OCI Resource Manager with Terraform**. A complete Terraform template is provided in `deployment/terraform/` that provisions:

1. **VCN** with public and private subnets
2. **Compute Instances** for BharatMart backend API (configurable count)
3. **Load Balancer** with health checks on `/api/health` endpoint
4. **Security Lists** with appropriate rules for Load Balancer and Compute instances
5. **Internet Gateway** and **NAT Gateway** for network connectivity

#### Quick Deployment Steps
1. Create ZIP file of `deployment/terraform/` directory
2. Upload to OCI Resource Manager (Console → Resource Manager → Stacks)
3. Fill in required variables (compartment_id, image_id, ssh_public_key)
4. Run Plan and Apply jobs to provision infrastructure
5. Deploy BharatMart application on the Compute instances
6. Configure environment variables and start the application

For detailed deployment instructions, see `deployment/terraform/README.md`.

This operational setup generates various manual tasks that demonstrate toil concepts for SRE learning.

---

## 1. Concept Overview

**Toil** is manual, repetitive, automatable work that:

* Is triggered by events rather than engineering intention
* Doesn't create long-term value
* Scales linearly with service growth
* Happens frequently and consumes engineering time

Understanding and reducing toil is fundamental to SRE practice. It allows teams to focus on engineering work that improves reliability, rather than repetitive operational tasks.

Key principles:

* Toil consumes error budget without improving reliability
* Automation is the primary mechanism for toil reduction
* Not all manual work is toil (some requires human judgment)
* Toil reduction is an ongoing process, not a one-time effort

---

## 2. How This Applies to IT Engineers and Developers

### IT Engineers

* Identify manual infrastructure tasks that can be automated
* Recognize patterns in repetitive operational work
* Prioritize automation efforts based on impact
* Design self-healing systems to reduce toil

### Developers

* Build automation for common operational tasks
* Create tooling that prevents manual intervention
* Design systems that require minimal manual maintenance
* Write code that self-reports issues and suggests fixes

### Unified View

```
Manual Work → Identify Toil → Prioritize → Automate → Focus on Engineering
```

---

## 3. Key Concepts

### 3.1 Characteristics of Toil

Toil has specific characteristics:

* **Repetitive** – Same task performed multiple times
* **Manual** – Requires human intervention
* **Automatable** – Can be done by scripts or systems
* **Event-driven** – Triggered by incidents or alerts
* **No long-term value** – Doesn't improve system design

### Examples of Toil in BharatMart Operations:

* Restarting BharatMart API when CPU spikes occur
* Manually checking logs for common error patterns
* Updating inventory levels in database by hand during peak seasons
* Responding to the same alert repeatedly without fixing root cause
* Manually scaling instances during traffic spikes

---

## 3.2 Toil vs. Engineering Work

#### Toil
* Restarting services
* Checking logs manually
* Updating configurations by hand
* Responding to repeated alerts

#### Engineering Work
* Designing automated scaling
* Building monitoring dashboards
* Creating self-healing systems
* Fixing root causes of issues

Key distinction: Engineering work creates long-term value; toil is temporary fixes.

---

## 3.3 Automation Prioritization

Automation should be prioritized when a task is:

* **Frequent** – Happens daily or weekly
* **Time-consuming** – Takes significant engineering time
* **Error-prone** – Manual execution leads to mistakes
* **High-impact** – Failures cause significant issues

Tasks that are rare or require deep human judgment are *not* good automation candidates.

---

## 4. Real-World Examples

### Example 1 — Manual API Restarts in BharatMart

#### Scenario

BharatMart API instances experience CPU spikes during peak shopping hours, requiring manual restarts.

* **Toil:** Engineer manually SSHes to instance and restarts API service
* **Frequency:** Daily during peak traffic periods
* **Time:** 5-10 minutes per incident
* **Solution:** Automated health checks with auto-restart or auto-scaling configured
* **Impact:** Frees up 30-60 minutes daily for engineering work

---

### Example 2 — Manual Log Checking for Errors

#### Scenario

SREs manually check BharatMart application logs for 500 errors multiple times per day.

* **Toil:** Engineer runs grep commands or logs into OCI Logging Service to search for errors
* **Frequency:** Multiple times per day during incidents
* **Time:** 10-15 minutes per check
* **Solution:** Automated alarms configured in OCI based on log patterns, alerts sent to on-call
* **Impact:** Eliminates reactive log checking, enables proactive response

---

### Example 3 — Manual Inventory Updates

#### Scenario

Inventory levels need manual updates during peak shopping seasons for BharatMart.

* **Toil:** Database administrator manually updates inventory quantities in database
* **Frequency:** Weekly during peak shopping periods
* **Time:** 30-60 minutes per update session
* **Solution:** Automated inventory sync from external systems or API-driven updates
* **Impact:** Reduces errors and frees up DBA time for optimization work

---

## 5. Case Study

### Scenario: Reducing Toil in BharatMart Operations

#### Problem

BharatMart operations team spends significant time on manual tasks:

* 2 hours/day manually checking logs for order placement errors
* 1 hour/day restarting API instances during CPU spikes
* 30 minutes/day manually updating configuration files
* 45 minutes/day responding to repeated alerts for the same issues

#### Total toil

~4 hours/day = 20 hours/week = ~80 hours/month

---

### Analysis

#### Toil Identification

1. **Manual log checking** (High toil score: Time=3, Frequency=5, Score=15)
   * Happens multiple times daily
   * Repetitive pattern matching
   * Automatable with log-based metrics and alarms

2. **Manual API restarts** (High toil score: Time=2, Frequency=4, Score=8)
   * Triggered by CPU spikes
   * Should be automated with health checks and auto-scaling
   * Root cause should be addressed

3. **Manual configuration updates** (Medium toil score: Time=4, Frequency=2, Score=8)
   * Infrequent but time-consuming
   * Should use Infrastructure as Code (IaC)
   * OCI Resource Manager or Terraform can automate

4. **Repeated alert responses** (High toil score: Time=3, Frequency=5, Score=15)
   * Same alerts firing repeatedly
   * Root cause not being fixed
   * Need better alert tuning and incident response

---

### Solution

#### Automation Strategy

1. **Automated Log Monitoring**
   * Create logging-based metrics for error patterns
   * Configure OCI alarms for order placement failures
   * Set up dashboards for proactive monitoring

2. **Automated Instance Management**
   * Configure OCI auto-scaling for API instances
   * Set up health checks with automatic recovery
   * Implement instance pools for high availability

3. **Infrastructure as Code**
   * Use OCI Resource Manager for configuration management
   * Automate deployment and configuration updates
   * Version control for infrastructure changes

4. **Alert Tuning**
   * Fix root causes of repeated alerts
   * Implement alert fatigue reduction strategies
   * Create runbooks for common alert responses

---

### Result

* **Toil Reduction:** 80 hours/month → 10 hours/month (87.5% reduction)
* **Engineering Time:** Freed up 70 hours/month for reliability improvements
* **System Reliability:** Improved through automation and root cause fixes
* **Team Morale:** Reduced burnout from repetitive tasks

---

## 6. Architecture / Workflow Diagrams

### Diagram 1 — Toil Identification Process

```
Manual Task → Analyze Characteristics → Calculate Toil Score → Prioritize → Automate
```

### Diagram 2 — Toil Reduction Impact

```
Before: 80% Toil, 20% Engineering
After:  20% Toil, 80% Engineering
```

### Diagram 3 — Automation Prioritization

```
High Frequency + High Time = Highest Priority
Low Frequency + Low Time = Lowest Priority
```

---

## 7. Best Practices

* Regularly audit operational tasks for toil
* Measure toil using time and frequency metrics
* Prioritize automation based on toil scores
* Fix root causes, don't just automate symptoms
* Invest in Infrastructure as Code (IaC)
* Build self-healing systems
* Create runbooks for remaining manual tasks

---

## 8. Common Mistakes

* Automating everything without prioritization
* Not fixing root causes, just automating symptoms
* Ignoring rare but critical manual tasks
* Automating tasks that require human judgment
* Not measuring toil reduction impact

---

## 9. Additional Notes

* Toil reduction is an iterative process
* Start with highest toil score items
* Measure success by engineering time freed up
* Toil reduction directly impacts error budget management
* This topic prepares you for automation topics in subsequent sessions

