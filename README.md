# **📘 5-Day SRE + OCI Course Outline**

---

## ✅ **Day 1: SRE Fundamentals, Culture, and Cloud-Native Alignment with OCI**

### **Understanding Concepts (Theory)**

* What is Site Reliability Engineering?
* History of SRE (Google, evolution into mainstream)
* SRE vs DevOps vs Platform Engineering
* Principles of SRE (SLI, SLO, Error Budget)
* OCI architecture overview

  * Core OCI Concepts
  * Compartments
  * Tenancy

### **Demonstration Only**

* Create a multi-region OCI tenancy (practical setup)
* Launch & configure OCI Compute instances using Infrastructure-as-Code (Terraform)

### **Hands-on Labs**

* Configure Cloud Shell and SDKs for automation
* Set up Identity Domains and IAM policies for SRE access control

---

## ✅ **Day 2: SLIs, SLOs, Error Budgets – Design & Monitoring in OCI**

### **Understanding Concepts (Theory)**

* Defining and implementing SLOs/SLIs for cloud-native services
* Error budgets and policy enforcement
* How OCI integrates with SRE principles

### **Demonstration Only**

* Define SLI/SLOs for a sample web app running on OCI Load Balancer + Compute
* Error budget breach simulation using OCI Health Checks and failover testing

### **Hands-on Labs**

* Set up OCI Monitoring (Metrics Explorer, Alarms)
* Create custom metrics using OCI Telemetry SDKs
* Implement alerting workflows with OCI Notifications and email/SMS triggers

---

## ✅ **Day 3: Reducing Toil, Observability, and Automating with OCI**

### **Understanding Concepts (Theory)**

* What is toil and why it must be reduced
* Observability: metrics, logs, traces
* The role of automation in SRE and types of automation

### **Demonstration Only**

* Automate Compute instance provisioning using OCI Resource Manager (Terraform)

### **Hands-on Labs**

* Reduce toil using Scheduled Functions (OCI Functions + Events)
* Use OCI Logging service for real-time log stream analysis
* Create logging metrics, push to OCI Monitoring, and visualize

---

## ✅ **Day 4: High Availability, Resilience, and Failure Testing on OCI**

### **Understanding Concepts (Theory)**

* Understanding Anti-fragility and Chaos Engineering
* OCI services for high availability and resilience
* Learning from failure, Postmortem culture

### **Demonstration Only**

* Simulate region failure and test cross-region DR
* Run failure injection using OCI CLI and chaos simulation scripts

### **Hands-on Labs**

* Set up a scalable app using OCI Load Balancer + Auto Scaling
* Use OCI Vault + Secrets for configuration resilience
* Conduct a blameless postmortem on simulated outage

---

## ✅ **Day 5: SRE Organizational Impact, Tools, APIs & Secure SRE**

### **Understanding Concepts (Theory)**

* Organizational shift to SRE
* Blameless culture, on-call design, rotational health
* Secure automation practices
* SRE in the context of ITIL, Agile, DevOps

### **Hands-on Labs**

* Implement OCI Service Connector Hub for automated incident response
* Secure automation using OCI Vault + dynamic secrets
* Use OCI REST APIs to build an SRE dashboard
* Deploy a sample OCI DevOps Pipeline with SLIs embedded

---

## ✅ **End of Day 5: Review, Q&A, Sample Exam**

* Sample SRE Foundation Exam Q&A
* Review case studies of SRE adoption in cloud
* Feedback, improvements, and scaling strategy

