# Day 3: Reduce Toil Using Scheduled Functions (OCI Functions + Events) - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will use OCI Functions and Events to automate scheduled tasks and reduce toil.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* OCI Functions and Events access
* Understanding of toil concepts from previous topics

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Understand how scheduled automation reduces toil
* Create an OCI Function for automated tasks
* Configure OCI Events for scheduled function execution
* Automate repetitive operational tasks
* Measure toil reduction from automation

---

## 2. Background Concepts

### 2.1 Scheduled Automation for Toil Reduction

Scheduled automation eliminates toil by:

* Running routine tasks automatically on a schedule
* Eliminating manual intervention for repetitive work
* Ensuring consistency in task execution
* Freeing engineering time for valuable work

### 2.2 OCI Functions and Events

**OCI Functions:** Serverless function execution platform
* Write functions in Python, Node.js, Java, Go, etc.
* Pay only for execution time
* Automatic scaling

**OCI Events:** Event routing and scheduling service
* Trigger functions on schedules
* Route events to functions
* Integrate with OCI services

Together, they enable scheduled automation for toil reduction.

---

## 3. Hands-On Task 1 — Create an OCI Function

#### Purpose

Create a function that automates a repetitive operational task.

**Example Use Case:** Automated log cleanup, health check automation, metric collection, etc.

### Steps:

1. **Create Function Application:**
   - Navigate to **OCI Console → Developer Services → Functions → Applications**
   - Click **Create Application**
   - Name: `<student-id>-automation-app`
   - Compartment: Select your compartment
   - VCN: Select VCN with Internet Gateway
   - Subnets: Select public subnet
   - Click **Create**

2. **Create Function:**
   - Click on your application
   - Click **Create Function**
   - Choose **Cloud Shell** or **Local Development** approach
   - Follow prompts to create function

**Example Function (Python) - Automated Health Check:**
```python
import io
import json
import requests

def handler(ctx, data: io.BytesIO=None):
    """
    Automated health check function for BharatMart API
    Reduces toil of manual health checks
    """
    try:
        # Health check endpoint
        response = requests.get('http://<your-lb-ip>/api/health', timeout=5)
        
        result = {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'status_code': response.status_code,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Log result or send to monitoring
        print(json.dumps(result))
        
        return result
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
```

3. **Deploy Function:**
   - Deploy function using `fn deploy` command
   - Verify function is active

---

## 4. Hands-On Task 2 — Configure Scheduled Event

#### Purpose

Configure OCI Events to trigger the function on a schedule.

### Steps:

1. **Create Event Rule:**
   - Navigate to **OCI Console → Application Integration → Events Service → Rules**
   - Click **Create Rule**
   - Name: `<student-id>-scheduled-health-check`
   - Display Name: `Scheduled Health Check Automation`

2. **Configure Conditions:**
   - **Condition:** Select **Event Type: Schedule**
   - **Schedule:** Set schedule (e.g., every 5 minutes, daily at 2 AM)
   - Example: `cron(0/5 * * * ? *)` for every 5 minutes

3. **Configure Actions:**
   - **Action Type:** Functions
   - **Function Application:** Select your function application
   - **Function:** Select your health check function
   - Click **Create**

---

## 5. Hands-On Task 3 — Verify Automation

#### Purpose

Verify that the scheduled automation is working and reducing toil.

### Steps:

1. **Monitor Function Executions:**
   - Navigate to **OCI Console → Developer Services → Functions → Applications**
   - Click your application
   - View function invocations
   - Verify function is executing on schedule

2. **Check Function Logs:**
   - View function logs to verify execution
   - Check for successful health checks
   - Identify any errors

3. **Measure Toil Reduction:**
   - Calculate time saved: Manual checks (e.g., 5 min/day) vs Automated (0 min/day)
   - Document frequency: How often task was done manually
   - Calculate toil score reduction

---

## 6. Summary of the Hands-On

In this exercise, you:

* Created an OCI Function for automated tasks
* Configured OCI Events for scheduled execution
* Automated a repetitive operational task
* Measured toil reduction from automation

This demonstrates how scheduled automation eliminates toil in day-to-day operations.

---

## 7. Additional Use Cases

Consider automating:

* Log cleanup and rotation
* Database backup verification
* Metric collection and reporting
* Configuration validation
* Health checks and status reporting
* Inventory synchronization
* Report generation

---

## 8. Solutions Key (Instructor Reference)

### ✔ Solution Key — Task 1: Function Creation

#### Expected Configuration:

* Application: `<student-id>-automation-app`
* Function: Health check or similar automation function
* Runtime: Python, Node.js, or Java
* Status: Active

### ✔ Solution Key — Task 2: Event Configuration

#### Expected Settings:

* Rule: `<student-id>-scheduled-health-check`
* Schedule: Configured (e.g., every 5 minutes)
* Action: Function invocation
* Status: Active

### ✔ Solution Key — Task 3: Verification

#### Expected Results:

* Function executing on schedule
* Logs showing successful executions
* Toil reduction measured and documented

---

## End of Hands-On Document

