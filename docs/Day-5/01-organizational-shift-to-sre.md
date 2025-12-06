# Day 5: Organizational Shift to SRE

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that organizations are transitioning to SRE practices.

**Assumed Context:**
* **Organizations** adopting SRE principles
* **Teams** restructuring to include SRE
* **Culture** evolving to support SRE practices

---

## 1. Concept Overview

**Organizational shift to SRE** involves transitioning from traditional operations models to SRE practices. This transformation requires changes in:

* **Team Structure** - New SRE teams and roles
* **Culture** - Embracing SRE principles and practices
* **Processes** - New workflows for reliability engineering
* **Tools and Practices** - Adopting SRE methodologies

Key principles:

* **Reliability as Objective** - Reliability is a primary goal
* **Measurable Goals** - Use SLIs and SLOs
* **Clear Roles** - Define responsibilities
* **Open Communication** - Share information transparently
* **Continuous Improvement** - Learn and iterate

---

## 2. Key Concepts

### 2.1 Reliability as an Objective

Treating reliability as a primary business and technical goal, not just a side effect.

**Traditional Approach:**
* "Make it work" → Reliability implicit
* No measurement or goals

**SRE Approach:**
* Define reliability targets (SLOs)
* Measure and track reliability (SLIs)
* Manage error budget

### 2.2 Team Roles and Charters

**SRE Team:**
* Owns: Reliability engineering, observability, incident response, SLOs
* Responsibilities: Define SLIs/SLOs, build observability, respond to incidents

**Development Team:**
* Owns: Feature development, application code
* Responsibilities: Build features meeting reliability requirements, implement observability

**IT/Platform Team:**
* Owns: Infrastructure, deployment, platforms
* Responsibilities: Provide reliable infrastructure, automate deployments

### 2.3 Communication Protocols

**Incident Communication:**
* Quick acknowledgment
* Regular status updates
* Clear resolution announcements

**SLO Reviews:**
* Regular SLO review meetings
* Error budget discussions
* Trade-off decisions

**Knowledge Sharing:**
* Postmortems shared across teams
* Best practices documentation
* Cross-team training

---

## 3. Real-World Examples

### Example 1 — Defining Reliability Objectives for BharatMart

**Process:**
1. Business requirements analysis
2. Define SLIs (availability, latency, error rate)
3. Set SLOs (99.9% availability, P95 < 500ms)
4. Establish error budgets

**Result:** Clear, measurable reliability objectives

---

## 4. Additional Notes

* Organizational shift is gradual, not overnight
* Clear roles and charters prevent confusion
* Communication is essential for success
* This topic prepares you for building SRE culture

