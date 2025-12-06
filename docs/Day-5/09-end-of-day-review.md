# Day 5: Review, Q&A, Sample Exam

### Audience Context: All Participants

---

## 0. Deployment Assumptions

This is a review and Q&A session at the end of Day 5. Students should have completed all previous topics and hands-on labs.

**Assumed Context:**
* Students have completed Days 1-5 content
* Hands-on labs have been practiced
* BharatMart platform has been used throughout the training
* OCI services have been explored and configured

---

## 1. Course Review

### 1.1 Day 1: SRE Fundamentals, Culture, and Cloud-Native Alignment with OCI

**Key Topics:**
* What is Site Reliability Engineering?
* History of SRE (Google, evolution into mainstream)
* SRE vs DevOps vs Platform Engineering
* Principles of SRE (SLI, SLO, Error Budget)
* OCI Architecture Overview

---

### 1.2 Day 2: SLIs, SLOs, Error Budgets – Design & Monitoring in OCI

**Key Topics:**
* Defining and implementing SLOs/SLIs for cloud-native services
* Error budgets and policy enforcement
* How OCI integrates with SRE principles
* OCI Monitoring setup
* Custom metrics integration
* Alerting workflows

---

### 1.3 Day 3: Reducing Toil, Observability, and Automating with OCI

**Key Topics:**
* What is toil and why it must be reduced
* Observability: metrics, logs, traces
* The role of automation in SRE
* OCI Logging service
* Logging-based metrics
* Scheduled automation

---

### 1.4 Day 4: High Availability, Resilience, and Failure Testing on OCI

**Key Topics:**
* Understanding Anti-fragility and Chaos Engineering
* OCI services for high availability and resilience
* Learning from failure, Postmortem culture
* Load Balancer + Auto Scaling
* OCI Vault for secrets management
* Blameless postmortems

---

### 1.5 Day 5: SRE Organizational Impact, Tools, APIs & Secure SRE

**Key Topics:**
* Organizational shift to SRE
* Blameless culture, on-call design, rotational health
* Secure automation practices
* SRE in the context of ITIL, Agile, DevOps
* OCI Service Connector Hub
* OCI REST APIs
* DevOps pipelines with SLIs

---

## 2. Sample SRE Foundation Exam Q&A

### 2.1 Question 1: SLIs and SLOs

**Q: What is the difference between an SLI and an SLO?**

**A:** 
- **SLI (Service Level Indicator):** A metric that measures a specific aspect of service reliability (e.g., uptime percentage, request latency, error rate)
- **SLO (Service Level Objective):** A target value for an SLI (e.g., 99.9% uptime, P95 latency < 500ms)

---

### 2.2 Question 2: Error Budget

**Q: If you have an availability SLO of 99.9%, what is your error budget?**

**A:** Error budget = 100% - SLO = 100% - 99.9% = 0.1%

For a monthly window: 0.1% of 30 days × 24 hours × 60 minutes = 43.2 minutes of downtime allowed per month.

---

### 2.3 Question 3: Toil

**Q: What is toil and why should it be reduced?**

**A:** 
- **Toil:** Manual, repetitive, automatable work that doesn't create long-term value
- **Why reduce:** Toil consumes error budget without improving reliability, takes time away from engineering work, and leads to burnout

---

### 2.4 Question 4: Postmortems

**Q: What is a blameless postmortem?**

**A:** A blameless postmortem focuses on systems and processes rather than individuals. It assumes good intentions, understands decision context, and uses incidents to improve systems rather than assign blame.

---

### 2.5 Question 5: High Availability

**Q: How do Fault Domains help achieve high availability?**

**A:** Fault Domains provide hardware isolation within an Availability Domain. By deploying instances across multiple Fault Domains, a failure in one FD doesn't affect instances in other FDs, ensuring service continuity.

---

## 3. Review Case Studies of SRE Adoption in Cloud

### 3.1 Case Study 1: E-commerce Platform Reliability

**Scenario:** BharatMart e-commerce platform required improved reliability.

**Approach:**
* Defined SLIs/SLOs (99.9% availability, P95 < 500ms)
* Implemented comprehensive monitoring
* Automated incident response
* Reduced toil through automation

**Results:**
* 99.95% availability achieved
* Error budget protected
* Team productivity increased

---

### 3.2 Case Study 2: Organizational SRE Transformation

**Scenario:** Organization transitioning from traditional operations to SRE.

**Approach:**
* Established SRE team
* Defined team charters
* Implemented SLO framework
* Built observability infrastructure

**Results:**
* Clear reliability objectives
* Improved incident response
* Better collaboration between teams

---

## 4. Feedback, Improvements, and Scaling Strategy

### 4.1 Course Feedback

**Please provide feedback on:**
* Course content relevance
* Hands-on lab effectiveness
* Instructor clarity
* Time allocation
* Additional topics needed

---

### 4.2 Improvement Opportunities

**Future Enhancements:**
* Additional hands-on exercises
* More case studies
* Advanced topics
* Real-world scenarios

---

### 4.3 Scaling Strategy

**Next Steps:**
* Apply SRE practices to your organization
* Start with SLIs/SLOs for key services
* Build observability infrastructure
* Establish incident response procedures
* Continuously improve and iterate

---

## 5. Additional Resources

### 5.1 Recommended Reading

* "Site Reliability Engineering" by Google SRE Team
* "The Site Reliability Workbook" by Google SRE Team
* OCI Documentation and Best Practices

---

### 5.2 Practice Exercises

* Define SLIs/SLOs for your services
* Set up monitoring and alerting
* Practice incident response
* Conduct postmortems

---

## End of Review Document

