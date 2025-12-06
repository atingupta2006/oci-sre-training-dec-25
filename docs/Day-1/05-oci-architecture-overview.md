# Day 1: OCI Architecture Overview

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** will be deployed on OCI to demonstrate architecture concepts.

**Assumed Context:**

* **BharatMart platform** will be deployed on OCI Compute instances
* **OCI infrastructure** will be provisioned (VCNs, Load Balancers, etc.)
* **OCI services** (Monitoring, Logging) will be used for observability

---

## 1. Concept Overview

OCI (Oracle Cloud Infrastructure) core architecture provides the foundational building blocks required to deploy reliable, secure, and scalable applications. For IT engineers and developers, understanding OCI's architectural components is essential for designing applications that meet SRE-driven reliability targets such as availability, latency, and resilience.

OCI's design principles include:

* **High isolation** through compartments and VCNs
* **Predictable performance** via bare-metal and virtual compute
* **Network-level flexibility** similar to on-prem data centres
* **Integrated observability** through metrics, logs, and traces

This topic focuses on the most important architectural elements relevant for SRE.

---

## 2. How This Applies to IT Engineers and Developers

#### IT Engineers

* Helps design network layouts, routing, and security configurations.
* Supports creating reliable deployment targets (subnets, gateways, load balancers).
* Enables capacity planning using compute shapes, block volumes, and autoscaling.

#### Developers

* Understand how application behaviour interacts with OCI components.
* Know where latency originates (LB → VM → DB → external calls).
* Learn how logs, metrics, traces flow through OCI.

#### Unified View

```
Application Code → Runs on Compute → Connected via VCN → Observed via Logging/Monitoring
```

---

## 3. Core OCI Concepts

#### Compartments

OCI uses compartments to isolate resources for permissions, billing, and governance.

Compartments provide:

* **Logical organization:** Group related resources together
* **Access control:** IAM policies apply at compartment level
* **Billing isolation:** Track costs per compartment
* **Resource limits:** Apply quotas per compartment

#### Tenancy

The tenancy is your root compartment and represents your Oracle Cloud account. All resources are organized within the tenancy and its compartments.

Key tenancy concepts:

* **Region:** Geographic location (e.g., us-ashburn-1, eu-frankfurt-1)
* **Availability Domain (AD):** Independent data centers within a region
* **Fault Domain (FD):** Logical groups of hardware within an AD that share power and network

---

## 4. Key Principles

#### Principle 1: Compartmentalisation

OCI uses compartments to isolate resources for permissions, billing, and governance.

#### Principle 2: Software-Defined Networking

VCNs offer complete control of routing, subnets, gateways, and firewall rules.

#### Principle 3: Compute Architecture

Multiple compute options allow predictable performance:

* VM Standard Shapes
* Flexible VM Shapes
* Bare Metal Instances
* Autoscaling Instance Pools

#### Principle 4: High-Availability Services

Load balancers, subnets, fault domains, and AD/FD placement ensure reliability.

#### Principle 5: Integrated Observability

Logs + metrics + alarms allow SRE to detect degradation early.

---

## 5. BharatMart Platform on OCI

BharatMart demonstrates this architecture:

* **Application:** BharatMart API runs on OCI Compute instances
* **Network:** Connected via VCN with public/private subnets
* **Database:** OCI Autonomous Database or Supabase
* **Observability:** Metrics at `/metrics`, health at `/api/health`, logs for monitoring
* **Load Balancing:** OCI Load Balancer routes traffic to healthy API instances

---

## 6. Real-World Examples

### Example 1 — OCI Load Balancer Backend Failures

#### Scenario

BharatMart API instances are all placed in the same Fault Domain.

#### Problem
* All backend VMs in same Fault Domain
* Host maintenance in that Fault Domain causes complete outage
* No redundancy across fault domains

#### SRE Solution

* Distribute BharatMart API instances across multiple Fault Domains
* OCI Load Balancer health checks route traffic only to healthy backends
* Single fault domain failure no longer causes complete service outage

---

## 7. Architecture Diagram: OCI Core Components

```
                           🌐 Public Internet
                                   |
                                   |
                          +--------v---------+
                          |   Internet Gateway|
                          +--------+---------+
                                   |
                                   |
                    ================== VCN ==================
                                   |
                     +-------------v-------------+
                     |        PUBLIC SUBNET       |
                     |                             |
                     |   +---------------------+   |
                     |   |   Public Load        |   |
                     |   |   Balancer (LB)      |   |
                     |   |   - Public IP        |   |
                     |   |   - TLS Termination |   |
                     |   +----------+----------+   |
                     |              |              |
                     +--------------|--------------+
                                    |
                                    |
                     +--------------v--------------+
                     |        PRIVATE SUBNET        |
                     |                              |
                     |   +----------------------+   |
                     |   |   Application VMs    |   |
                     |   |   - No Public IP     |   |
                     |   |   - Auto Scaling     |   |
                     |   |   - Conn Pooling     |   |
                     |   +----------+-----------+   |
                     |              |               |
                     +--------------|---------------+
                                    |
                                    |
                     +--------------v--------------+
                     |        PRIVATE ENDPOINT      |
                     |                              |
                     |   +----------------------+   |
                     |   |  Autonomous Database |   |
                     |   |  - No Public Access  |   |
                     |   |  - Managed HA        |   |
                     |   |  - Private IP Only   |   |
                     |   +----------------------+   |
                     |                              |
                     +------------------------------+
```

---

## 8. Diagram: High Availability Placement

```
==========================  REGION  ==========================

+------------------------+        +------------------------+
|  Availability Domain 1 |        |  Availability Domain 2 |
|                        |        |                        |
|  +------------------+  |        |  +------------------+  |
|  | Fault Domain 1   |  |        |  | Fault Domain 1   |  |
|  | (Rack Group A)  |  |        |  | (Rack Group D)  |  |
|  +------------------+  |        |  +------------------+  |
|                        |        |                        |
|  +------------------+  |        |  +------------------+  |
|  | Fault Domain 2   |  |        |  | Fault Domain 2   |  |
|  | (Rack Group B)  |  |        |  | (Rack Group E)  |  |
|  +------------------+  |        |  +------------------+  |
|                        |        |                        |
|  +------------------+  |        |  +------------------+  |
|  | Fault Domain 3   |  |        |  | Fault Domain 3   |  |
|  | (Rack Group C)  |  |        |  | (Rack Group F)  |  |
|  +------------------+  |        |  +------------------+  |
+------------------------+        +------------------------+

==============================================================
```

---

## 9. Best Practices

* Always deploy across multiple ADs/Fault Domains.
* Use private subnets for application tier.
* Use appropriate gateways (IGW/NAT/Service Gateway).
* Enable VCN flow logs for network diagnostics.
* Ensure Cloud Agent is enabled for full metrics.
* Use instance pools instead of standalone VMs.

---

## 10. Common Mistakes

* Placing all compute resources in a single AD.
* Missing NAT gateway in private subnet.
* Not enabling health checks for LB backends.
* Using incorrectly sized compute shapes.

---

## 11. Additional Notes

* OCI's architecture offers deeper control compared to many clouds.
* SRE depends heavily on these core components for reliability.
* Understanding OCI architecture is essential for designing reliable systems.
* BharatMart platform demonstrates these architecture principles in practice.

