# Day 4: Conduct a Blameless Postmortem on Simulated Outage - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will practice incident response and create a postmortem document.

**Prerequisites:**
* BharatMart deployed with monitoring
* Access to metrics and logs
* Understanding of postmortem structure

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Practice incident detection and response
* Investigate root cause using observability data
* Document incident timeline
* Create a blameless postmortem document
* Identify actionable improvement items

---

## 2. Background Concepts

### 2.1 Incident Response Process

* Detection → Acknowledgment → Investigation → Mitigation → Resolution → Postmortem

### 2.2 Blameless Postmortem

Focus on systems and processes, not individuals. Learn and improve.

---

## 3. Hands-On Task 1 — Run Simulated Incident Play

#### Purpose

Practice responding to a simulated incident.

### Scenario

**Incident:** BharatMart API experiencing high latency and errors.

**Initial Symptoms:**
* Users report slow page loads
* P95 latency above 500ms
* Error rate increasing

### Steps

#### Step 1: Incident Detection (10 minutes)

1. **Check Monitoring Dashboard:**
   * Review API latency metrics
   * Check error rates
   * Identify anomalies

2. **Check Application Metrics:**
   ```bash
   curl http://<api-url>/metrics | grep -E "http_request_duration_seconds|http_requests_total"
   ```

3. **Check Application Logs:**
   * Review recent error logs
   * Look for patterns or spikes

**Document:**
* Time detected: __________
* Initial symptoms: __________
* Severity level: P0/P1/P2/P3

---

#### Step 2: Investigation (15 minutes)

1. **Analyze Metrics:**
   * Which endpoints are affected?
   * When did latency start increasing?
   * Correlate with error rates

2. **Review Logs:**
   * Look for error messages
   * Check for database issues
   * Review chaos engineering status

3. **Check Infrastructure:**
   * CPU, memory utilization
   * Network metrics
   * Database connections

**Document:**
* Root cause identified: __________
* Evidence: __________
* Contributing factors: __________

---

#### Step 3: Mitigation and Resolution (10 minutes)

1. **Apply Mitigation:**
   * Based on root cause, apply fix
   * Examples: Disable chaos, restart services, scale up

2. **Verify Resolution:**
   * Check metrics return to normal
   * Verify no residual issues
   * Confirm user impact resolved

**Document:**
* Mitigation applied: __________
* Resolution time: __________
* Verification: __________

---

## 4. Hands-On Task 2 — Create Postmortem Document

#### Purpose

Document the incident following blameless postmortem structure.

### Postmortem Template

Fill out the following sections:

---

#### 1. Incident Summary

**Brief Description:**
[2-3 sentences describing what happened]

**Timeline:**
- Detected: __________
- Resolved: __________
- Duration: __________ minutes

**Impact:**
- Users Affected: __________
- Features Impacted: __________
- Severity: P0/P1/P2/P3

---

#### 2. Detailed Timeline

| Time | Event |
|------|-------|
|      |       |
|      |       |
|      |       |

---

#### 3. Root Cause Analysis

**What Caused the Incident:**
[Detailed explanation]

**Contributing Factors:**
[Factors that enabled the issue]

**Why It Happened:**
[Context and background]

---

#### 4. Impact Assessment

**Users Affected:**
[Number or percentage]

**Business Impact:**
[Revenue, reputation, etc.]

**Error Budget Impact:**
[Percentage consumed]

---

#### 5. What Went Well

- [Example: Quick detection via monitoring]
- [Example: Effective team communication]
- [Example: Rapid mitigation]

---

#### 6. What Didn't Go Well

- [Example: Investigation took longer than expected]
- [Example: Missing monitoring for specific metric]
- [Example: Unclear procedures]

---

#### 7. Action Items

| Action Item | Owner | Priority | Due Date | Status |
|-------------|-------|----------|----------|--------|
|             |       |          |          |        |
|             |       |          |          |        |

---

#### 8. Lessons Learned

- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]

---

## 5. Summary of the Hands-On

In this exercise, you:

* Practiced incident detection and investigation
* Applied mitigation and resolution steps
* Created a blameless postmortem document
* Identified actionable improvement items
* Practiced learning from failures

These skills are essential for effective incident response and continuous improvement.

---

## 6. Solutions Key (Instructor Reference)

### Expected Postmortem Quality:

* **Blameless language** throughout
* **Focus on systems** and processes
* **Specific action items** with owners and dates
* **Clear timeline** with timestamps
* **Honest assessment** of what went well/not well
* **Actionable improvements** identified

---

## End of Hands-On Document

