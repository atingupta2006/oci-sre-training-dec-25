# Day 2: Error Budgets and Policy Enforcement

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this topic, we assume that **BharatMart e-commerce platform** is already deployed on OCI with SLIs and SLOs defined.

**Assumed Context:**
* **SLIs and SLOs** have been defined for BharatMart (see previous topic)
* **Metrics** are available for tracking error budget consumption
* **Monitoring** is set up to track SLO compliance

---

## 1. Concept Overview

Error budgets quantify the **acceptable failure** within SLO targets. They balance innovation (new features) with stability (reliability work).

Error budgets govern **how much unreliability is tolerable** before releases must pause and stability work must take priority.

---

## 2. How Error Budgets Work

```
If SLO = 99.9% → allowable errors = 0.1% of requests
```

Example calculation:

* Monthly traffic: 2,000,000 requests
* SLO: 99.5% success rate
* Allowed failures: 0.5% = 10,000 failures per month

---

## 3. Error Budget Policy Enforcement

When error budget is consumed:

#### Warning threshold (50% consumed):

* Slow down new feature releases
* Increase focus on reliability improvements
* Review recent changes that may have impacted reliability

#### Critical threshold (75% consumed):

* Pause new feature releases
* Mandatory focus on stability and bug fixes
* Incident review and remediation

#### Error budget exhausted (100% consumed):

* Complete release freeze
* All engineering effort on reliability
* Post-mortem required for SLO violations
* SLO review and potential adjustment

---

## 4. Policy Enforcement in Practice

#### Automated Enforcement

* CI/CD pipeline checks error budget before deployment
* Automated alerts when error budget burn rate is high
* Dashboard showing error budget status visible to all teams

#### Manual Governance

* Weekly SRE review of error budget status
* Monthly stakeholder review of SLO compliance
* Quarterly SLO review and adjustment based on business needs

---

## 5. Real-World Example: BharatMart Error Budget Policy

**SLO:** Order API success rate ≥ 99.5%

**Error Budget:** 0.5% = 10,000 failures per month (assuming 2M monthly requests)

**Policy:**
* **50% consumed (5,000 failures):** Warning alert, slow feature velocity
* **75% consumed (7,500 failures):** Release pause, focus on stability
* **100% consumed (10,000 failures):** Full freeze, mandatory post-mortem

**Monitoring:**
* Track via `/metrics` endpoint: `http_requests_total{status_code=~"5.."}`
* Error budget dashboard showing consumption over time
* Automated alerts when thresholds crossed

---

## 6. Key Takeaways

* Error budgets balance velocity and reliability
* Clear policies guide release decisions
* Automation enforces error budget policies
* Regular reviews ensure policies align with business needs
* Error budgets provide objective criteria for release decisions

