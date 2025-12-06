# Day 1: History of SRE (Google, Evolution into Mainstream)

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** will be used throughout the training to demonstrate SRE concepts and OCI integration.

**Assumed Context:**

* **BharatMart platform** demonstrates modern SRE practices
* **OCI** provides SRE-friendly infrastructure and services
* **SRE principles** evolved over two decades to reach current state

---

## 1. Origins at Google

Site Reliability Engineering was pioneered by Google in the early 2000s. Google faced a challenge: as their services scaled to millions of users, traditional operations models broke down. They needed a new approach that combined software engineering practices with operations expertise.

#### Key Milestones

* **2003-2004:** Ben Treynor Sloss forms Google's first SRE team
* **2003-2010:** SRE practices refined through managing Google's massive-scale services (Search, Gmail, Maps)
* **2016:** Google publishes "Site Reliability Engineering: How Google Runs Production Systems" book, making SRE practices widely accessible
* **2016-Present:** SRE adoption spreads across tech industry (Netflix, LinkedIn, Amazon, Microsoft, etc.)
* **2018-Present:** SRE becomes mainstream in enterprise IT, not just tech companies

---

## 2. Evolution into Mainstream

#### Phase 1: Tech Giants (2010-2015)
* Large tech companies (Netflix, LinkedIn, Twitter) adopt SRE
* Focus on internet-scale services
* Emphasis on automation and reliability at scale

#### Phase 2: Enterprise Adoption (2016-2020)
* Traditional enterprises begin adopting SRE principles
* Integration with DevOps practices
* Cloud providers offer SRE-friendly services

#### Phase 3: Cloud-Native Era (2020-Present)
* Cloud-native architectures make SRE principles more accessible
* Platform Engineering emerges as complementary discipline
* SRE becomes standard practice for cloud operations

---

## 3. Why SRE Matters Today

SRE practices are now essential because:

* **Cloud complexity:** Modern cloud architectures require systematic reliability engineering
* **User expectations:** Users expect 99.9%+ uptime from critical services
* **Business impact:** Downtime directly impacts revenue and reputation
* **Scale:** Applications must handle unpredictable traffic patterns
* **Automation:** Infrastructure as Code and automation make SRE practices achievable

---

## 4. SRE in Oracle Cloud Infrastructure (OCI)

OCI was designed with SRE principles in mind:

* **Reliability:** Built-in high availability through Availability Domains and Fault Domains
* **Observability:** Integrated monitoring, logging, and tracing services
* **Automation:** Resource Manager (Terraform), Functions, Events for infrastructure automation
* **Measurability:** Comprehensive metrics and SLI/SLO capabilities

### How OCI Supports SRE

#### Built-in High Availability

OCI's architecture provides:

* Multiple Availability Domains within a region
* Fault Domains for redundancy within an Availability Domain
* Automatic failover capabilities through Load Balancers

#### Integrated Observability

OCI services enable SRE practices:

* **OCI Monitoring:** Collect and query metrics for SLI definition
* **OCI Logging:** Centralized log collection and analysis
* **OCI Dashboards:** Visualize metrics and SLO compliance
* **OCI Alarms:** Automated alerting on SLO violations

#### Infrastructure Automation

OCI enables Infrastructure as Code:

* **Resource Manager:** Managed Terraform execution
* **OCI Functions:** Serverless automation
* **OCI Events:** Event-driven automation

These capabilities make it easier to implement SRE principles using OCI, as demonstrated throughout this training with the BharatMart platform.

