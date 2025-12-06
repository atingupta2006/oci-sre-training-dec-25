# Day 4: OCI Services for High Availability and Resilience

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** is deployed on OCI with high availability requirements.

**Assumed Context:**
* **BharatMart** deployed on OCI Compute instances with Load Balancer
* **Multiple Availability Domains and Fault Domains** available
* **OCI services** configured for high availability

---

## 1. Concept Overview

**High Availability (HA)** is the ability of a system to remain operational and accessible even when individual components fail. OCI provides built-in services and features that enable high availability without custom engineering.

Key OCI services for HA:

* Availability Domains and Fault Domains
* Load Balancers with health checks
* Auto Scaling
* Instance Pools
* Database redundancy options

---

## 2. OCI Services for High Availability

### 2.1 Availability Domains and Fault Domains

**Availability Domains (ADs):**
* Physically separate data centers within a region
* Each AD has independent power, cooling, and networking
* Multiple ADs provide region-level redundancy

**Fault Domains (FDs):**
* Logical grouping of hardware within an Availability Domain
* Each FD has independent power and hardware
* OCI provides 3 Fault Domains per Availability Domain

**HA Strategy:**
* Deploy instances across multiple Fault Domains
* Use multiple Availability Domains for region-level redundancy
* Ensure no single point of failure

### 2.2 Load Balancers

**Features:**
* Automatic traffic distribution
* Health checks for backend instances
* Automatic failover when backends become unhealthy
* SSL termination
* Session persistence

**BharatMart Implementation:**
* Load Balancer distributes traffic to API instances
* Health checks on `/api/health` endpoint
* Automatic removal of unhealthy backends
* Traffic routed only to healthy instances

### 2.3 Auto Scaling

**Features:**
* Automatic scaling based on metrics (CPU, memory, request rate)
* Scale up during traffic spikes
* Scale down during low traffic
* Cost optimization through automatic capacity adjustment

**BharatMart Implementation:**
* Auto-scaling based on CPU utilization
* Maintains SLO compliance during peak shopping hours
* Automatic capacity adjustment based on actual demand

### 2.4 Instance Pools

**Features:**
* Groups of Compute instances managed together
* Automatic instance replacement
* Uniform configuration across instances
* Easy scaling and management

---

## 3. High Availability Architecture

### Example: BharatMart HA Deployment

```
OCI Load Balancer
       |
       ├── Backend Set 1
       │     ├── Instance 1 (Fault Domain 1)
       │     ├── Instance 2 (Fault Domain 2)
       │     └── Instance 3 (Fault Domain 3)
       │
       └── Health Checks on /api/health
              |
              └── Automatic Failover
```

**Benefits:**
* Single Fault Domain failure doesn't cause outage
* Health checks ensure only healthy instances receive traffic
* Automatic replacement of failed instances

---

## 4. Resilience Services

### 4.1 OCI Vault

**Purpose:** Secure secrets management for resilience

**Features:**
* Encrypted secret storage
* Secret versioning
* Rotation without downtime
* Audit logging

### 4.2 Backups and Snapshots

**Block Volume Backups:**
* Automated backups
* Point-in-time recovery
* Cross-region backup copies

**Database Backups:**
* OCI Autonomous Database: Automated daily backups
* 60-day retention
* Point-in-time recovery

---

## 5. Best Practices

* Deploy across multiple Fault Domains
* Use Load Balancers for traffic distribution
* Configure health checks on all backends
* Enable auto-scaling for dynamic capacity
* Use instance pools for uniform management
* Implement automated backups
* Store secrets in OCI Vault
* Test failover procedures regularly

---

## 6. Additional Notes

* OCI services provide HA capabilities without custom engineering
* Proper configuration ensures high availability
* Regular testing validates HA design
* This topic prepares you for HA labs

