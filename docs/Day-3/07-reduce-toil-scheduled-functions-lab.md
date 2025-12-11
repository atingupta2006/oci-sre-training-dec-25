# Day 3: Reduce Toil Using Scheduled Functions (OCI Functions + Events)

## **0. Deployment Assumptions**

This lab uses **local development on an Ubuntu VM**, with:

* Docker installed using `get-docker`
* Fn CLI
* OCI CLI
* A Function Application already created in OCI Console
* OCI Events Rule to schedule the function

**Prerequisites:**

* OCI Tenancy with permissions to use Functions, Events, and Logging
* VCN + Subnet configured for Functions
* Ubuntu VM with Docker + Fn CLI + OCI CLI installed
* OCIR login configured

---

## **1. Objective of This Hands‑On**

By the end of this hands-on, participants will:

✔ Understand how scheduled automation reduces operational toil
✔ Create an automated health‑check function using Python
✔ Deploy the function to OCI using Fn CLI
✔ Configure OCI Events to trigger the function on a schedule
✔ Verify automation via logs and invocations
✔ Measure toil reduction achieved through automation

---

## **2. Background Concepts**

### **2.1 How Scheduled Automation Reduces Toil**

Automation eliminates repetitive manual tasks by:

* Running tasks automatically on a schedule
* Ensuring consistent execution
* Removing human error
* Freeing engineers for value‑added work

### **2.2 OCI Functions + OCI Events**

**OCI Functions**
A fully managed FaaS (Functions‑as‑a‑Service) platform.
Key benefits:

* Serverless execution
* Auto‑scaling
* Pay per execution
* Supports Python, Node.js, Java, Go

**OCI Events**
Event routing + scheduling platform.
Used for:

* Triggering scheduled tasks
* Forwarding service events to Functions
* Workflow automation

Together, they enable scheduled operational automation.

---

# **3. Hands‑On Task 1 — Create the Health‑Check OCI Function (Local Development)**

### **Purpose**

We will create a Python OCI Function that performs a periodic health check against a backend service or load balancer endpoint.

---

## **3.1 Create Application (OCI Console)**

Performed **once**, from the UI.

1. Go to **Developer Services → Functions → Applications**
2. Click **Create Application**
3. Name:

```
<student-id>-automation-app
```

4. Choose your compartment
5. Select VCN with **Internet Gateway**
6. Select **public subnet**
7. Click **Create**

---

# **3.2 Function Creation (Local Ubuntu VM)**

All steps below run on your **local Ubuntu VM**.

### **Step 1 — Create working directory**

```bash
mkdir health-check-fn && cd health-check-fn
```

### **Step 2 — Initialize function project**

```bash
fn init --runtime python health-check
cd health-check
```

This creates:

```
func.py
func.yaml
requirements.txt
```

---

# **3.3 Replace Function Code with Working Health‑Check Function**

Open:

```bash
nano func.py
```

Replace contents with:

```python
import io
import json
import logging
from datetime import datetime
import requests
from fdk import response

def handler(ctx, data: io.BytesIO = None):
    url = "http://<your-lb-ip-or-service>/api/health"
    result = {}

    try:
        r = requests.get(url, timeout=5)
        result = {
            "target": url,
            "status": "healthy" if r.status_code == 200 else "unhealthy",
            "status_code": r.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        result = {
            "target": url,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

    logging.getLogger().info(json.dumps(result))

    return response.Response(
        ctx,
        response_data=json.dumps(result),
        headers={"Content-Type": "application/json"}
    )
```

---

# **3.4 Update requirements.txt**

```bash
nano requirements.txt
```

Replace with:

```
fdk
requests
```

---

# **3.5 Verify func.yaml**

A minimal working config:

```
schema_version: 20180708
name: health-check
version: 0.0.1
runtime: python
entrypoint: /python/bin/fdk /function/func.py handler
memory: 256
```

---

# **3.6 Build & Deploy the Function**

Make sure Docker + OCIR login + FN_REGISTRY are configured.

### **Build**

```bash
fn build
```

### **Deploy**

```bash
fn list apps
fn deploy --app <app-name>
```

### **Invoke manually (test)**

```bash
fn invoke <app-name> health-check
```

Expected output:

```json
{"status": "healthy", ... }
```

---

# **4. Hands‑On Task 2 — Configure Scheduled Event Rule**

### **Purpose**

Trigger the health-check function automatically on a schedule.

---

## **4.1 Create Event Rule (OCI Console)**

1. Go to:
   **Application Integration → Events Service → Rules**
2. Click **Create Rule**
3. Provide:

```
Name: scheduled-<app-name>-health-check
Display Name: Scheduled Health Check Automation
```

---

## **4.2 Configure Condition**

Select:

* **Event Type: Schedule**

---

## **4.3 Configure Action**

* **Action Type:** Functions
* **Application:** `<app-name>`
* **Function:** `health-check`

Click **Create**.

---

# **5. Hands‑On Task 3 — Verification of Automation**

### **5.1 View Function Invocations**

Navigate:
**Developer Services → Functions → Applications → Your Application → Functions → health-check**

You should see invocation counts increasing over time.

---

### **5.2 View Logs in Logging Service**

Function logs appear under:

**Observability & Management → Logging → Log Groups**

Look for:

```
<app-name>-functions log group
```

Check for:

* Scheduled executions
* Health check results
* Any errors

---
