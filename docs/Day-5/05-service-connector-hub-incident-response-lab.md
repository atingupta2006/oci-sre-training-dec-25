# Day 5: Implement OCI Service Connector Hub for Automated Incident Response - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will configure OCI Service Connector Hub for automated incident response.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* BharatMart deployed on OCI Compute instances
* OCI Monitoring alarms configured (from Day 2 labs)
* OCI Functions service access
* OCI CLI configured and working

**Assumed Deployment:**
* BharatMart application running and monitored
* At least one monitoring alarm configured (e.g., CPU utilization alarm)
* Load Balancer health checks active

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Understand OCI Service Connector Hub architecture
* Configure service connector for automated incident response
* Route monitoring alarms to response functions
* Create OCI Function for automated incident handling
* Automate incident notification and response workflows
* Verify automated incident response is working

---

## 2. Background Concepts

### 2.1 OCI Service Connector Hub

**Service Connector Hub** enables automated routing of service events to target services for processing without writing custom integration code.

**Key Features:**
* Event routing from sources (Monitoring, Logging, Streaming) to targets (Functions, Notifications, Object Storage)
* No custom integration code needed
* Automatic event transformation and filtering
* Built-in retry and error handling

**Use Cases:**
* Automate incident response from alarm triggers
* Route alarms to functions for automated remediation
* Stream events to processing services
* Archive logs and events to Object Storage

### 2.2 Incident Response Automation

**Automated Incident Response** reduces mean time to resolution (MTTR) by:

* Immediately triggering response actions when alarms fire
* Executing automated remediation (restart services, scale resources, etc.)
* Sending notifications to on-call engineers
* Logging incident details for postmortem analysis

### 2.3 Architecture Flow

```
BharatMart Application
    ↓
OCI Monitoring (Metrics/Alarms)
    ↓ (Alarm triggers)
Service Connector Hub
    ↓ (Routes alarm event)
OCI Function (Incident Response)
    ↓ (Actions)
- Send notification
- Log incident
- Trigger remediation (if needed)
```

---

## 3. Hands-On Task 1 — Create Incident Response Function

#### Purpose

Create an OCI Function that will receive alarm events and perform automated incident response actions.

### Steps:

#### Step 1: Create Function Application

1. **Navigate to Functions:**
   - Go to **OCI Console → Developer Services → Functions → Applications**
   - Select your compartment
   - Click **Create Application**

2. **Configure Application:**
   - **Name:** `<student-id>-incident-response-app`
   - **VCN:** Select VCN with Internet Gateway (or create new)
   - **Subnets:** Select public subnet(s)
   - **Logging:** Enable logging (optional but recommended)
   - Click **Create**

3. **Note the Application OCID** for later use.

#### Step 2: Configure Function Authentication

1. **Create Dynamic Group:**
   - Go to **Identity → Dynamic Groups**
   - Click **Create Dynamic Group**
   - **Name:** `<student-id>-incident-response-functions`
   - **Rule:**
     ```
     resource.type = 'fnfunc'
     resource.compartment.id = '<your-compartment-ocid>'
     ```
   - Click **Create**

2. **Create Policy for Dynamic Group:**
   - Go to **Identity → Policies**
   - Click **Create Policy**
   - **Name:** `<student-id>-incident-response-policy`
   - **Policy Statements:**
     ```
     Allow dynamic-group <student-id>-incident-response-functions to manage objects in compartment <compartment-name>
     Allow dynamic-group <student-id>-incident-response-functions to use ons-topics in compartment <compartment-name>
     Allow dynamic-group <student-id>-incident-response-functions to read alarms in compartment <compartment-name>
     ```
   - Click **Create**

#### Step 3: Create Function Code

1. **Navigate to your Application:**
   - Click on `<student-id>-incident-response-app`

2. **Create Function:**
   - Click **Create Function**
   - Select **Cloud Shell** or **Local Development**
   - Choose **Python 3.9** runtime
   - Name: `incident-response-handler`

> **📝 Note: Repository Function Example Available**
> 
> A complete incident response function example is available in the application repository:
> - **Location:** `scripts/oci-service-connector-hub/incident-response-function/`
> - **Files:** `func.py`, `func.yaml`, `requirements.txt`
> - **Features:** Enhanced error handling, ONS notification integration, logging
> - **Documentation:** See `scripts/oci-service-connector-hub/README.md`
> 
> You can use this example as a starting point, or follow the steps below to create your own.

3. **Create Function Code:**

   Create `func.py`:
   ```python
   import io
   import json
   import oci
   import logging

   # Configure logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   def handler(ctx, data: io.BytesIO = None):
       """
       Incident response handler for BharatMart alarms
       Processes alarm events from Service Connector Hub
       """
       try:
           # Parse incoming alarm event
           if data:
               event_data = json.loads(data.read().decode('utf-8'))
               logger.info(f"Received alarm event: {json.dumps(event_data, indent=2)}")
           else:
               # Test event structure
               event_data = {
                   "alarmId": "test-alarm-id",
                   "message": "Test alarm event",
                   "severity": "CRITICAL"
               }

           # Extract alarm information
           alarm_id = event_data.get("alarmId", "unknown")
           message = event_data.get("message", "No message")
           severity = event_data.get("severity", "UNKNOWN")
           timestamp = event_data.get("timestamp", "")

           # Log incident details
           incident_log = {
               "incident_id": alarm_id,
               "timestamp": timestamp,
               "severity": severity,
               "message": message,
               "service": "BharatMart",
               "status": "acknowledged"
           }

           logger.info(f"Incident logged: {incident_log}")

           # Send notification (optional - requires ONS topic)
           try:
               ons = oci.ons.NotificationDataPlaneClient({})
               topic_id = ctx.get("TOPIC_OCID", "")
               if topic_id:
                   ons.publish_message(
                       topic_id=topic_id,
                       message_details=oci.ons.models.MessageDetails(
                           title=f"BharatMart Incident: {severity}",
                           body=f"Alarm: {message}\nTime: {timestamp}"
                       )
                   )
                   logger.info(f"Notification sent to topic: {topic_id}")
           except Exception as e:
               logger.warning(f"Could not send notification: {e}")

           # Return response
           return {
               "status": "success",
               "incident_id": alarm_id,
               "actions_taken": [
                   "incident_logged",
                   "notification_sent" if topic_id else "notification_skipped"
               ],
               "message": f"Incident {alarm_id} processed successfully"
           }

       except Exception as e:
           logger.error(f"Error processing incident: {e}")
           return {
               "status": "error",
               "message": str(e)
           }
   ```

   Create `func.yaml`:
   ```yaml
   schema_version: 20180708
   name: incident-response-handler
   version: 0.0.1
   runtime: python
   entrypoint: /python/bin/fdk /function/func.py handler
   memory: 256
   timeout: 30
   ```

4. **Deploy Function:**
   ```bash
   # From Cloud Shell or local machine with OCI CLI configured
   cd <function-directory>
   fn deploy --app <student-id>-incident-response-app
   ```

   Expected output:
   ```
   Deploying incident-response-handler to app: <student-id>-incident-response-app
   ...
   Successfully deployed function: incident-response-handler
   ```

#### Step 4: Test Function

1. **Invoke Function Manually:**
   ```bash
   echo '{"alarmId":"test-123","message":"Test alarm","severity":"CRITICAL","timestamp":"2024-01-15T10:00:00Z"}' | \
   fn invoke <student-id>-incident-response-app incident-response-handler
   ```

2. **Verify Function Logs:**
   - Go to **OCI Console → Developer Services → Functions → Applications**
   - Click your application → Functions → incident-response-handler
   - Click **View Logs** to see function execution logs

   Expected log output:
   ```
   INFO: Received alarm event: {"alarmId":"test-123",...}
   INFO: Incident logged: {"incident_id":"test-123",...}
   ```

---

## 4. Hands-On Task 2 — Configure Service Connector

#### Purpose

Create a Service Connector that routes monitoring alarms to the incident response function.

> **📝 Note: Infrastructure as Code Option Available**
> 
> You can also create the Service Connector using Terraform (Infrastructure as Code). The application repository includes a Terraform example:
> - **Location:** `scripts/oci-service-connector-hub/service-connector-terraform.tf`
> - **Configuration:** Complete Service Connector Hub resource definition
> - **Integration:** Works with the incident response function
> - **Documentation:** See `scripts/oci-service-connector-hub/README.md`
> 
> **To use Terraform approach:**
> 1. Copy `service-connector-terraform.tf` to your Terraform configuration
> 2. Set variables: `function_ocid`, `compartment_id`, etc.
> 3. Run `terraform apply`
> 
> The manual steps below (using OCI Console) are recommended for learning. The Terraform approach is better for automation and version control.

### Steps:

#### Step 1: Create Service Connector

1. **Navigate to Service Connector Hub:**
   - Go to **OCI Console → Application Integration → Service Connector Hub**
   - Select your compartment
   - Click **Create Connector**

2. **Configure Basic Information:**
   - **Name:** `<student-id>-incident-response-connector`
   - **Description:** `Routes BharatMart monitoring alarms to incident response function`
   - **Compartment:** Select your compartment
   - Click **Next**

#### Step 2: Configure Source (Monitoring Alarms)

1. **Select Source:**
   - **Source Type:** Monitoring
   - Click **Next**

2. **Configure Monitoring Source:**
   - **Namespace:** `oci_computeagent` (for Compute metrics) or `custom.bharatmart` (for custom metrics)
   - **Compartment:** Select compartment containing your alarms
   - **Resource Group:** Leave empty (all resources) or specify resource group
   - Click **Next**

   **Note:** The connector will route alarm state change events (firing, clearing) from all alarms in the compartment.

#### Step 3: Configure Target (Functions)

1. **Select Target:**
   - **Target Type:** Functions
   - Click **Next**

2. **Configure Function Target:**
   - **Function Application:** Select `<student-id>-incident-response-app`
   - **Function:** Select `incident-response-handler`
   - **Function Invoke Endpoint:** Automatically populated
   - Click **Next**

#### Step 4: Review and Create

1. **Review Configuration:**
   - Verify source is set to Monitoring
   - Verify target is set to your function
   - Review policy requirements

2. **Policy Check:**
   Service Connector needs a policy. Create if not exists:
   ```
   Allow service servicconnector to use functions-family in compartment <compartment-name>
   Allow service servicconnector to read metrics in compartment <compartment-name>
   Allow service servicconnector to read alarms in compartment <compartment-name>
   ```

3. **Create Connector:**
   - Click **Create**
   - Wait for connector to be in **Active** state

#### Step 5: Verify Connector Status

1. **Check Connector State:**
   - Go to Service Connector Hub
   - Find your connector
   - Verify **State** is **Active**

2. **View Connector Details:**
   - Click on connector name
   - Review source and target configuration
   - Note the connector OCID for reference

---

## 5. Hands-On Task 3 — Test Automated Incident Response

#### Purpose

Trigger a test alarm to verify the automated incident response workflow.

### Steps:

#### Step 1: Trigger Test Alarm

1. **Option 1: Use Existing Alarm**
   - If you have an existing alarm from Day 2 labs, temporarily modify its threshold to trigger it

2. **Option 2: Create Test Alarm**
   - Go to **OCI Console → Observability & Management → Alarms**
   - Click **Create Alarm**
   - **Name:** `<student-id>-test-incident-alarm`
   - **Metric:** `CpuUtilization` (oci_computeagent namespace)
   - **Trigger:** When `mean` > `10` (low threshold for easy triggering)
   - **Compartment:** Select your compartment
   - Click **Create**
   - Wait 1-2 minutes for alarm to evaluate and potentially fire

#### Step 2: Monitor Alarm State

1. **Check Alarm Status:**
   - Go to **Alarms**
   - Find your test alarm
   - Wait until status changes to **Firing**

2. **View Alarm Details:**
   - Click on alarm name
   - Note the alarm state change timestamp

#### Step 3: Verify Function Invocation

1. **Check Function Logs:**
   - Go to **Functions → Applications → `<student-id>-incident-response-app`**
   - Click **Functions → incident-response-handler**
   - Click **View Logs**
   - Look for recent invocations with alarm event data

   Expected log entry:
   ```
   INFO: Received alarm event: {
     "alarmId": "ocid1.alarm...",
     "message": "Alarm <alarm-name> is now FIRING",
     "severity": "CRITICAL",
     "timestamp": "2024-01-15T10:30:00Z"
   }
   ```

2. **Check Function Metrics:**
   - In function details, view **Metrics** tab
   - Verify function invocations count increased

#### Step 4: Verify Incident Logging

1. **Check Function Output:**
   - Review function logs for successful incident logging message

2. **Check Notifications (if configured):**
   - If ONS topic was configured, verify notification was sent
   - Go to **Notifications → Topics** to check messages

---

## 6. Hands-On Task 4 — Enhance Incident Response (Optional)

#### Purpose

Add more sophisticated incident response actions.

### Steps:

#### Option 1: Add Auto-Scaling Response

Modify function to trigger auto-scaling when CPU alarm fires:

```python
# Add to handler function
if severity == "CRITICAL" and "CpuUtilization" in message:
    # Trigger auto-scaling (if configured)
    logger.info("High CPU detected - recommending scale-out")
    # Could call OCI API to update instance pool size
```

#### Option 2: Add Incident Dashboard Update

Send incident data to a logging service for dashboard visibility:

```python
# Add to handler function
import oci.loggingingestion

logging_client = oci.loggingingestion.LoggingClient({})
logging_client.put_logs(
    log_id="<log-ocid>",
    put_logs_details=oci.loggingingestion.models.PutLogsDetails(
        specversion="1.0",
        log_entry_batches=[
            oci.loggingingestion.models.LogEntryBatch(
                entries=[{
                    "data": incident_log,
                    "id": alarm_id,
                    "time": timestamp
                }]
            )
        ]
    )
)
```

---

## 7. Summary of the Hands-On

In this exercise, you:

* Created an OCI Function for automated incident response
* Configured dynamic groups and policies for function access
* Created a Service Connector to route alarms to functions
* Tested automated incident response workflow
* Verified alarm events trigger function invocations
* Enhanced incident logging and notification

This demonstrates how Service Connector Hub enables automated incident response, reducing MTTR and operational toil.

---

## 8. Additional Use Cases

Consider implementing:

* **Multi-level Response:** Different functions for different severity levels
* **Incident Triage:** Route to different teams based on alarm type
* **Remediation Actions:** Auto-restart services, scale resources, failover
* **Incident Correlation:** Aggregate multiple alarms into single incident
* **Postmortem Automation:** Auto-generate incident reports

---

## 9. Troubleshooting

### Function Not Invoked

* Verify Service Connector is **Active**
* Check connector policies are correct
* Verify alarm is in correct compartment
* Check function logs for errors

### Function Errors

* Verify function has required permissions (dynamic group policy)
* Check function code for syntax errors
* Verify OCI SDK is properly configured in function

### No Alarm Events

* Verify alarm actually fired (check alarm state)
* Wait 1-2 minutes for events to propagate
* Check Service Connector metrics for events received

---

## 10. Solutions Key (Instructor Reference)

### ✔ Solution Key — Task 1: Function Creation

#### Expected Configuration:

* Application: `<student-id>-incident-response-app`
* Function: `incident-response-handler`
* Runtime: Python 3.9
* Status: Active
* Dynamic Group: Configured with proper policies

### ✔ Solution Key — Task 2: Service Connector

#### Expected Settings:

* Connector: `<student-id>-incident-response-connector`
* Source: Monitoring (all alarms in compartment)
* Target: Function (`incident-response-handler`)
* State: Active

### ✔ Solution Key — Task 3: Testing

#### Expected Results:

* Alarm fires when threshold exceeded
* Function receives alarm event within 1-2 minutes
* Function logs show successful processing
* Incident logged with proper details

---

## End of Hands-On Document
