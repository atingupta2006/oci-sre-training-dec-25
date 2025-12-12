# Day 5: Blameless Culture, On-Call Design, Rotational Health

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** requires on-call coverage and team health management.

**Assumed Context:**
* **BharatMart** deployed in production with monitoring
* **On-call rotation** established or being established
* **Team health** considerations important

---

## 1. Concept Overview

**Blameless Culture** focuses on learning from failures by examining systems and processes rather than blaming individuals.

**On-Call Design** ensures 24/7 coverage while maintaining team sustainability.

**Rotational Health** monitors team workload and prevents burnout.

---

## 2. Key Concepts

### 2.1 Blameless Culture Principles

**Focus on Systems, Not People:**
* Assume good intentions
* Understand decision context
* Identify process gaps
* Use incidents to improve systems

**Learning from Failures:**
* Every incident is a learning opportunity
* Share knowledge across team
* Build organizational capability
* Prevent recurrence through improvement

### 2.2 On-Call Design

**Rotation Models:**
* **Primary/Secondary:** Primary responds first, secondary as backup
* **Follow-the-Sun:** Regional coverage across time zones
* **Weekend Rotation:** Separate weekend coverage

**Design Principles:**
* Fair distribution of on-call time
* Clear handoff procedures
* Defined escalation paths
* Reasonable workload

### 2.3 Managing Alert Fatigue

**Strategies:**
* Alert classification (Critical, High, Medium, Low)
* Alert tuning (appropriate thresholds)
* Alert filtering (actionable issues only)
* Runbook integration

### 2.4 Team Health Monitoring

**Metrics to Track:**
* On-call load (incidents per shift)
* Incident impact (frequency, duration)
* Work-life balance (time off, hours)
* Team satisfaction (surveys, retention)

**Health Indicators:**
* Healthy: Even distribution, reasonable workload, good balance
* Unhealthy: Uneven load, high frequency, burnout signs

---

## 3. Real-World Examples

### Example 1 — Designing On-Call Rotation for BharatMart

**Team:** 8 engineers
**Model:** Primary/Secondary, weekly rotation

**Result:** Fair distribution, 24/7 coverage, good work-life balance

---

### Example 2 — Reducing Alert Fatigue

**Problem:** 150+ alerts per day, causing fatigue

**Solution:**
* Alert classification (Critical: 5-10/day)
* Alert tuning (reduce false positives)
* Runbook integration

**Result:** 50-60 actionable alerts per day, improved productivity

---

## 4. Additional Notes

* Blameless culture enables learning
* On-call must be sustainable
* Team health is critical for long-term success
* This topic prepares you for on-call management

