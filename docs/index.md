# SRE Training Program - BharatMart Platform

Welcome to the comprehensive **5-Day SRE Training Program** built around the **BharatMart e-commerce platform** running on Oracle Cloud Infrastructure (OCI).

---

## 📘 About This Training

This training program provides:

- **Complete 5-Day SRE Curriculum** covering all essential SRE concepts
- **Hands-on Labs** with detailed step-by-step instructions
- **Practical Demonstrations** using OCI services
- **Real-world Examples** using the BharatMart application
- **Code-driven Documentation** with source references

### 🎯 Training Platform: BharatMart

**BharatMart** is a production-grade e-commerce platform specifically designed for SRE training. It demonstrates:

- **Observability:** Prometheus metrics, structured JSON logging, optional distributed tracing
- **Reliability:** Health endpoints, chaos engineering capabilities, multiple deployment modes
- **Automation:** Background workers, Infrastructure as Code examples, automated testing
- **Multi-tier Architecture:** Frontend, Backend API, Database, Cache, Workers

**Key Endpoints:**
- `/metrics` - Prometheus metrics
- `/api/health` - Health check endpoint
- `/api/system/info` - Comprehensive system information

---

## 📚 Course Structure

Each day is organized into three learning modules:

1. **Understanding Concepts (Theory)** - Core SRE concepts and principles
2. **Demonstrations** - Instructor-led practical demonstrations
3. **Hands-on Labs** - Step-by-step exercises for students

---

## 🎓 Day 1: SRE Fundamentals, Culture, and Cloud-Native Alignment with OCI

### Understanding Concepts (Theory)

- [What is Site Reliability Engineering?](Day-1/01-what-is-site-reliability-engineering.md)
- [History of SRE (Google, Evolution into Mainstream)](Day-1/02-history-of-sre.md)
- [SRE vs DevOps vs Platform Engineering](Day-1/03-sre-vs-devops-vs-platform-engineering.md)
- [Principles of SRE (SLI, SLO, Error Budget)](Day-1/04-principles-of-sre-sli-slo-error-budget.md)
- [OCI Architecture Overview](Day-1/05-oci-architecture-overview.md)

### Demonstrations

- [Create a Multi-Region OCI Tenancy (Practical Setup)](Day-1/06-multi-region-oci-tenancy-demo.md)
- [Launch & Configure OCI Compute Instances using Infrastructure-as-Code (Terraform)](Day-1/07-terraform-compute-instances-demo.md)

### Hands-on Labs

- [Configure Cloud Shell and SDKs for Automation](Day-1/08-configure-cloud-shell-sdks-lab.md)
- [Set up Identity Domains and IAM Policies for SRE Access Control](Day-1/09-identity-domains-iam-policies-lab.md)

➡️ **View Day 1 Overview:** [Day-1/index.md](Day-1/index.md)

---

## 🎓 Day 2: SLIs, SLOs, Error Budgets – Design & Monitoring in OCI

### Understanding Concepts (Theory)

- [Defining and Implementing SLOs/SLIs for Cloud-Native Services](Day-2/01-defining-slis-slos-cloud-native.md)
- [Error Budgets and Policy Enforcement](Day-2/02-error-budgets-policy-enforcement.md)
- [How OCI Integrates with SRE Principles](Day-2/03-oci-integrates-sre-principles.md)

### Demonstrations

- [Define SLI/SLOs for a Sample Web App Running on OCI Load Balancer + Compute](Day-2/04-define-sli-slos-demo.md)
- [Error Budget Breach Simulation Using OCI Health Checks and Failover Testing](Day-2/05-error-budget-breach-simulation-demo.md)

### Hands-on Labs

- [Set up OCI Monitoring (Metrics Explorer, Alarms)](Day-2/06-setup-oci-monitoring-lab.md)
- [Create Custom Metrics Using OCI Telemetry SDKs](Day-2/07-create-custom-metrics-telemetry-sdk-lab.md)
- [Implement Alerting Workflows with OCI Notifications and Email/SMS Triggers](Day-2/08-implement-alerting-workflows-lab.md)
- [Create Dashboards and Visualizations for SRE Observability](Day-2/09-dashboards-visualization-lab.md)

➡️ **View Day 2 Overview:** [Day-2/index.md](Day-2/index.md)

---

## 🎓 Day 3: Reducing Toil, Observability, and Automating with OCI

### Understanding Concepts (Theory)

- [What is Toil and Why It Must Be Reduced](Day-3/01-what-is-toil-why-reduce.md)
- [Observability: Metrics, Logs, Traces](Day-3/02-observability-metrics-logs-traces.md)
- [The Role of Automation in SRE and Types of Automation](Day-3/03-role-automation-sre-types.md)

### Demonstrations

- [Automate Compute Instance Provisioning using OCI Resource Manager (Terraform)](Day-3/04-terraform-resource-manager-demo.md)

### Hands-on Labs

- [Use OCI Logging Service for Real-Time Log Stream Analysis](Day-3/05-oci-logging-real-time-analysis-lab.md)
- [Create Logging Metrics, Push to OCI Monitoring, and Visualize](Day-3/06-logging-metrics-monitoring-lab.md)
- [Reduce Toil Using Scheduled Functions (OCI Functions + Events)](Day-3/07-reduce-toil-scheduled-functions-lab.md)

➡️ **View Day 3 Overview:** [Day-3/index.md](Day-3/index.md)

---

## 🎓 Day 4: High Availability, Resilience, and Failure Testing on OCI

### Understanding Concepts (Theory)

- [Understanding Anti-fragility and Chaos Engineering](Day-4/01-anti-fragility-chaos-engineering.md)
- [OCI Services for High Availability and Resilience](Day-4/02-oci-services-ha-resilience.md)
- [Learning from Failure, Postmortem Culture](Day-4/03-learning-from-failure-postmortem-culture.md)

### Demonstrations

- [Simulate Region Failure, Test Cross-Region DR](Day-4/04-simulate-region-failure-cross-region-dr-demo.md)
- [Run Failure Injection Using OCI CLI and Chaos Simulation Scripts](Day-4/05-failure-injection-oci-cli-chaos-demo.md)

### Hands-on Labs

- [Set up a Scalable App Using OCI Load Balancer + Auto Scaling](Day-4/06-load-balancer-auto-scaling-lab.md)
- [Use OCI Vault + Secrets for Configuration Resilience](Day-4/07-oci-vault-secrets-resilience-lab.md)
- [Conduct a Blameless Postmortem on Simulated Outage](Day-4/08-blameless-postmortem-simulated-outage-lab.md)

➡️ **View Day 4 Overview:** [Day-4/index.md](Day-4/index.md)

---

## 🎓 Day 5: SRE Organizational Impact, Tools, APIs & Secure SRE

### Understanding Concepts (Theory)

- [Organizational Shift to SRE](Day-5/01-organizational-shift-to-sre.md)
- [Blameless Culture, On-Call Design, Rotational Health](Day-5/02-blameless-culture-on-call-rotational-health.md)
- [Secure Automation Practices](Day-5/03-secure-automation-practices.md)
- [SRE in the Context of Other Frameworks (ITIL, Agile, DevOps)](Day-5/04-sre-context-itil-agile-devops.md)

### Hands-on Labs

- [Implement OCI Service Connector Hub for Automated Incident Response](Day-5/05-service-connector-hub-incident-response-lab.md)
- [Secure Automation Using OCI Vault, Dynamic Secrets](Day-5/06-secure-automation-vault-dynamic-secrets-lab.md)
- [Use OCI REST APIs to Build an SRE Dashboard](Day-5/07-oci-rest-apis-sre-dashboard-lab.md)
- [Deploy Sample OCI DevOps Pipeline with SLIs Embedded](Day-5/08-oci-devops-pipeline-slis-lab.md)

### End of Day 5: Review, Q&A, Sample Exam

- [Review, Q&A, Sample Exam](Day-5/09-end-of-day-review.md)

➡️ **View Day 5 Overview:** [Day-5/index.md](Day-5/index.md)

---

## 📖 Additional Resources

### Documentation Files

- [Enhancement Rules](ENHANCEMENT_RULES.md) - Guidelines for maintaining training materials
- [New Course Content](new-course-content.md) - Complete course outline reference

### Application Documentation

For detailed information about the BharatMart application:

- **GitHub Repository:** [oci-multi-tier-web-app-ecommerce](https://github.com/atingupta2006/oci-multi-tier-web-app-ecommerce)
- **Application Documentation:** See `docs/` folder in the repository
- **Configuration Guide:** See `config/` folder for deployment scenarios

---

## 🧭 Navigation Tips

- **Use the sidebar** to browse all topics and labs
- **Click any link above** to go directly to the topic or lab
- **Each day has an index file** (`Day-X/index.md`) with complete day overview
- **All labs include:**
  - Detailed step-by-step instructions
  - Code examples (Python, Bash, YAML)
  - Expected outputs and verification steps
  - Troubleshooting guides
  - Solution keys (instructor reference)

---

## 📊 Course Statistics

- **Total Days:** 5
- **Total Topics (Theory):** 17
- **Total Demonstrations:** 7
- **Total Hands-on Labs:** 18
- **Total Content Files:** 42 + 5 index files

---

## ✅ Course Completion Checklist

After completing all 5 days, students should be able to:

- [ ] Define SLIs, SLOs, and Error Budgets
- [ ] Set up monitoring and alerting in OCI
- [ ] Integrate custom metrics with OCI Monitoring
- [ ] Use OCI Logging for observability
- [ ] Reduce toil through automation
- [ ] Design high-availability architectures
- [ ] Implement chaos engineering practices
- [ ] Conduct blameless postmortems
- [ ] Build secure automation workflows
- [ ] Integrate SRE practices into CI/CD pipelines

---

## 🎯 Prerequisites

Before starting this training, students should have:

- Basic understanding of cloud computing concepts
- Familiarity with Linux command line
- Basic knowledge of Python or Bash scripting (helpful but not required)
- Access to an OCI tenancy with appropriate permissions
- Understanding of basic networking concepts

---

**Last Updated:** Training materials are continuously updated. All files include deployment assumptions and are ready for use.
