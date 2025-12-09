# Day 2: How OCI Integrates with SRE Principles

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** is deployed on OCI and uses OCI services for reliability.

**Assumed Context:**
* **BharatMart** deployed on OCI Compute instances
* **OCI services** (Monitoring, Load Balancer, Auto Scaling) are configured
* **BharatMart metrics** are integrated with OCI Monitoring

---

## 1. Concept Overview

OCI (Oracle Cloud Infrastructure) provides services and features that directly support SRE principles, making it easier to implement and maintain reliable systems.

---

## 2. OCI Services for SRE

#### 1. OCI Monitoring

**Purpose:** Collect, store, and query metrics for SLI definition

**SRE Benefits:**
* Default metrics from all OCI services (Compute, Load Balancer, Database)
* Custom metrics support for application-level SLIs
* Metric Explorer for querying and visualization
* Historical data for SLO baseline calculation

**Integration with BharatMart:**
* BharatMart metrics from `/metrics` endpoint can be ingested as custom metrics
* OCI Load Balancer metrics provide user-facing latency SLIs
* Combined infrastructure and application metrics for complete observability

#### 2. OCI Alarms and Notifications

**Purpose:** Automated alerting on SLO violations and reliability issues

**SRE Benefits:**
* Threshold alarms on any metric
* Composite alarms for complex conditions
* Multiple notification channels (email, SMS, webhooks)
* Integration with on-call systems (PagerDuty, etc.)

**Integration with BharatMart:**
* Alarms on BharatMart error rates from `/metrics` endpoint
* Alarms on Load Balancer health and latency
* Automated notifications to on-call SRE team

#### 3. OCI Load Balancer with Health Checks

**Purpose:** Automatic traffic routing and health-based failover

**SRE Benefits:**
* Health checks ensure only healthy backends receive traffic
* Automatic failover when backends become unhealthy
* Load Balancer metrics provide availability SLIs
* Reduces manual intervention (eliminates toil)

**Integration with BharatMart:**
* Health checks on `/api/health` endpoint
* Automatic removal of unhealthy API instances
* Load Balancer metrics track availability SLI

#### 4. OCI Availability Domains and Fault Domains

**Purpose:** Built-in redundancy for high availability

**SRE Benefits:**
* Deploy across multiple Fault Domains for redundancy
* Use multiple Availability Domains for regional redundancy
* Automatic isolation of failures
* Enables high availability without custom failover logic

**Integration with BharatMart:**
* BharatMart API instances deployed across Fault Domains
* Database in separate Availability Domain for isolation
* Enables 99.9%+ availability SLOs

#### 5. OCI Auto Scaling

**Purpose:** Automatic scaling based on metrics

**SRE Benefits:**
* Scale up during traffic spikes (protects SLOs)
* Scale down during low traffic (cost optimization)
* Reduces manual capacity planning toil
* Maintains performance under varying load

**Integration with BharatMart:**
* Auto-scaling based on CPU utilization or request rate
* Maintains SLO compliance during peak shopping hours
* Automatic capacity adjustment based on actual demand

#### 6. OCI Resource Manager (Terraform)

**Purpose:** Infrastructure as Code for reliable deployments

**SRE Benefits:**
* Repeatable, consistent infrastructure deployments
* Version-controlled infrastructure changes
* Reduces deployment errors and drift
* Enables disaster recovery through reproducible infrastructure

**Integration with BharatMart:**
* Terraform templates for BharatMart infrastructure
* Consistent deployments across environments
* Eliminates manual provisioning toil

---

## 3. OCI Architecture for SRE Best Practices

#### Multi-Region Deployment

```
Region 1 (Primary)          Region 2 (DR)
├─ AD1                      ├─ AD1
│  ├─ Fault Domain 1        │  ├─ Fault Domain 1
│  │  └─ BharatMart API     │  │  └─ BharatMart API
│  ├─ Fault Domain 2        │  ├─ Fault Domain 2
│  └─ Fault Domain 3        │  └─ Fault Domain 3
└─ Load Balancer            └─ Load Balancer
```

**SRE Benefits:**
* Regional redundancy for disaster recovery
* Cross-region failover capabilities
* Geographic distribution for latency optimization
* Enables higher availability SLOs (99.99%+)

#### Observability Architecture

```
BharatMart Application
    ├─→ Metrics (/metrics endpoint)
    │      └─→ OCI Monitoring (Custom Metrics)
    │
    ├─→ Logs (logs/api.log)
    │      └─→ OCI Logging Service
    │
    └─→ Health (/api/health)
           └─→ OCI Load Balancer Health Checks

OCI Infrastructure
    ├─→ Compute Metrics (CPU, Memory, Network)
    │      └─→ OCI Monitoring (Default Metrics)
    │
    ├─→ Load Balancer Metrics (Latency, Errors)
    │      └─→ OCI Monitoring (Default Metrics)
    │
    └─→ Database Metrics (Connections, Queries)
           └─→ OCI Monitoring (Default Metrics)
```

**SRE Benefits:**
* Unified observability across infrastructure and application
* Single source of truth for SLI measurement
* Integration between services for complete visibility
* Enables effective incident response and debugging

---

## 4. Key Takeaways

* OCI services are designed with SRE principles in mind
* Built-in high availability reduces custom engineering
* Integrated observability simplifies SLI/SLO implementation
* Automation features eliminate operational toil
* Multi-region capabilities enable higher availability targets
* OCI provides the foundation for implementing SRE practices effectively

