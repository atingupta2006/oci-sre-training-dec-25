# Day 1: SRE vs DevOps vs Platform Engineering

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** will be used throughout the training to demonstrate how different engineering disciplines interact.

**Assumed Context:**

* **BharatMart platform** demonstrates interactions between SRE, DevOps, and Platform Engineering
* **Different roles** contribute to reliability in different ways
* **Understanding distinctions** helps collaboration and ownership clarity

---

## 1. Concept Overview

This topic explains the distinctions and intersections between three engineering disciplines: **Site Reliability Engineering (SRE)**, **DevOps**, and **Platform Engineering**. IT engineers and developers often interact with all three without fully understanding how each contributes to system stability, scalability, and velocity.

The purpose is to offer a clear, structured comparison focused on:

* Responsibilities
* Objectives
* Methods of working
* How each discipline impacts system reliability

These distinctions help engineers collaborate more effectively and understand who owns which part of the reliability landscape.

---

## 2. How This Applies to IT Engineers and Developers

#### IT Engineers

* Helps clarify why SRE takes ownership of reliability rather than just performing ops tasks.
* Explains how Platform Engineering creates the internal tools and paved roads IT engineers rely on.
* Shows how DevOps practices impact deployment and operational workflows.

#### Developers

* Helps understand how their code interacts with SRE-defined reliability standards.
* Shows where Platform Engineering provides reusable components (CI/CD templates, infra modules).
* Illustrates how DevOps practices influence the development lifecycle.

#### Combined View

```
Developer: Writes and tests code
DevOps: Enables smooth build/deploy cycles
Platform Engineering: Provides internal tooling & reusable infrastructure
SRE: Ensures reliability, observability, and operational excellence
```

---

## 3. Key Principles

#### Site Reliability Engineering (SRE)

* Reliability as an engineering goal tracked through SLIs/SLOs.
* Focused on automation, observability, incident response, and capacity planning.
* Ensures systems behave consistently under varied load conditions.

#### DevOps

* Cultural and technical movement improving collaboration between dev and ops.
* Emphasises CI/CD, faster delivery, automation, and shared ownership.
* Focuses on deployment pipelines, environment consistency, and integration cycles.

#### Platform Engineering

* Builds internal platforms used by developers and engineers to deploy, test, and operate services.
* Provides reusable modules, paved roads, templates, and abstractions.
* Focuses on improving developer experience and productivity.

---

## 4. Diagram: Separation of Responsibilities

```
+-----------------+     +------------------+     +---------------------------+
|     SRE         |     |      DevOps      |     |    Platform Engineering   |
+-----------------+     +------------------+     +---------------------------+
| Reliability     |     | CI/CD Pipelines  |     | Internal Tools & Systems |
| Observability   |     | Deployment Flow  |     | Developer Enablement     |
| Incident Mgmt   |     | Integration      |     | Infrastructure Modules    |
| Capacity        |     | Automation       |     | Service Catalogs         |
+-----------------+     +------------------+     +---------------------------+
```

---

## 5. Real-World Examples

### Example 1 — Deployment Failure in BharatMart

#### Scenario

A new version of BharatMart is deployed, but the application becomes slow after deployment.

#### How Each Role Responds

* **Developers:** Push new version with new features.
* **DevOps:** Deploy to OCI Compute instances or OCI PaaS services using automated deployment processes
* **SRE:** Investigates latency spikes and error rates using:
  - Metrics endpoint: `/metrics` - Checking `http_request_duration_seconds`
  - Health endpoint: `/api/health` - Verifying service status
  - Logs: `logs/api.log` - Finding error patterns
* **Platform Engineering:** Provides reusable deployment templates and configuration patterns that include health checks by default.

#### BharatMart Implementation
- **DevOps:** Automated OCI deployments to single-VM or OCI PaaS
- **SRE:** Health checks endpoint (`/api/health`) used by OCI monitoring and deployment validation
- **Platform:** Reusable configuration templates for different deployment scenarios (single-VM, OCI PaaS)

### Example 2 — Scalability Requirements in BharatMart

#### Scenario

Traffic spikes occur during peak shopping periods, requiring system scaling.

#### How Each Role Responds

* **IT Engineers:** Notice traffic spikes and resource usage increases.
* **SRE:** Analyzes saturation metrics (CPU, memory, request rates) and error budgets to determine scaling needs.
* **Platform Engineering:** Provides flexible adapter pattern allowing easy switching:
  - Database: Supabase → PostgreSQL → OCI Autonomous
  - Cache: Memory → Redis → OCI Cache
  - Workers: In-process → Bull Queue → OCI Queue
* **DevOps:** Updates deployment configuration to use new adapters via environment variables.

#### BharatMart Implementation
- **Platform:** Adapter pattern that switches infrastructure via `DATABASE_TYPE`, `CACHE_TYPE`, `WORKER_MODE` environment variables
- **SRE:** Monitors metrics to determine when scaling is needed
- **DevOps:** Simple configuration change: `CACHE_TYPE=redis` switches from memory to Redis cache

---

## 6. Best Practices

* Clearly define ownership boundaries between SRE, DevOps, and Platform teams.
* Developers should rely on platform-provided tooling whenever possible.
* SRE should define measurable reliability goals (SLOs) for critical services.
* DevOps pipelines should integrate SRE checks (health checks, metrics validation).
* Platform teams should maintain consistency and reusability.

---

## 7. Common Mistakes

* Treating SRE as a replacement for DevOps or IT Ops.
* Assuming DevOps owns reliability.
* Developers bypassing platform tooling and creating inconsistent deployments.
* Lack of unified observability across teams.
* Missing SLOs leading to unclear reliability responsibilities.

---

## 8. Additional Notes

* Real-world organisations blend these roles differently, but the underlying principles remain consistent.
* Understanding these distinctions helps IT engineers and developers work effectively across cross-functional teams.
* BharatMart platform demonstrates how these roles interact in practice.

