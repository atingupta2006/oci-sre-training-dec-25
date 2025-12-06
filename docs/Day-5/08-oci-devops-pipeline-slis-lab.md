# Day 5: Deploy Sample OCI DevOps Pipeline with SLIs Embedded - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will create an OCI DevOps pipeline with reliability gates and SLI validation.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* OCI DevOps service enabled
* OCI CLI configured
* Understanding of CI/CD pipelines
* BharatMart application code repository
* Basic understanding of SLIs/SLOs from Day 2

**Assumed Deployment:**
* BharatMart application source code available
* Application deployed and monitored
* SLIs/SLOs defined for BharatMart
* Monitoring and alarms configured

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Understand OCI DevOps pipeline structure
* Create build and deployment pipelines
* Add reliability gates with SLI validation
* Configure pre-deployment checks
* Implement post-deployment validation
* Integrate SRE practices into CI/CD workflows

---

## 2. Background Concepts

### 2.1 OCI DevOps Pipeline

**OCI DevOps** provides CI/CD capabilities for OCI deployments with:

* **Build Pipelines:** Compile, test, and build applications
* **Deployment Pipelines:** Deploy to Compute, Container Engine, Functions
* **Artifact Repositories:** Store build artifacts
* **Triggers:** Automate pipeline execution (code commits, schedules)
* **Stages:** Modular pipeline stages for flexibility

### 2.2 Reliability Gates in CI/CD

**Reliability Gates** are checkpoints in deployment pipelines that validate:

#### Pre-Deployment:

* Error budget availability
* Current service health
* Test results
* Security scans

#### Post-Deployment:

* Health check verification
* Error rate monitoring
* Latency validation
* Rollback triggers

### 2.3 SLI Integration in Pipelines

**SLI Validation** ensures deployments don't breach SLOs:

* Check error budget before deployment
* Monitor metrics during deployment
* Validate SLIs after deployment
* Automatic rollback on SLO breach

---

## 3. Hands-On Task 1 — Create DevOps Project

#### Purpose

Set up OCI DevOps project and repository for BharatMart.

### Steps:

#### Step 1: Create DevOps Project

1. **Navigate to DevOps:**
   - Go to **OCI Console → Developer Services → DevOps → Projects**
   - Select your compartment
   - Click **Create Project**

2. **Configure Project:**
   - **Name:** `<student-id>-bharatmart-devops`
   - **Description:** `DevOps project for BharatMart with SRE gates`
   - **Compartment:** Select your compartment
   - Click **Create**

3. **Note the Project OCID** for later use.

#### Step 2: Create Code Repository (or Connect Existing)

1. **Navigate to Code Repositories:**
   - In your DevOps project, go to **Code Repositories**
   - Click **Create Repository**

2. **Create New Repository:**
   - **Name:** `bharatmart-app`
   - **Description:** `BharatMart application repository`
   - **Repository Type:** Mirrored (connect to external Git) or Private (OCI-hosted)
   - Click **Create**

3. **Option A - Connect External Repository:**
   - If you have existing Git repository (GitHub, GitLab):
     - Click **Mirror Repository**
     - Follow instructions to connect external repository

4. **Option B - Create New Repository:**
   - Clone repository:
     ```bash
     git clone <repository-url>
     cd bharatmart-app
     # Add your BharatMart code
     git add .
     git commit -m "Initial commit"
     git push
     ```

#### Step 3: Create Artifact Repository

1. **Navigate to Artifact Repositories:**
   - In your DevOps project, go to **Artifact Repositories**
   - Click **Create Repository**

2. **Configure Repository:**
   - **Name:** `bharatmart-artifacts`
   - **Repository Type:** Generic Artifacts
   - **Description:** `Build artifacts for BharatMart`
   - Click **Create**

---

## 4. Hands-On Task 2 — Create Build Pipeline

#### Purpose

Create build pipeline that compiles and tests BharatMart application.

### Steps:

#### Step 1: Create Build Pipeline

1. **Navigate to Build Pipelines:**
   - In your DevOps project, go to **Build Pipelines**
   - Click **Create Build Pipeline**

2. **Configure Pipeline:**
   - **Name:** `bharatmart-build-pipeline`
   - **Description:** `Build and test BharatMart application`
   - Click **Create**

#### Step 2: Add Build Stages

1. **Add Managed Build Stage:**
   - Click **Add Stage**
   - Select **Managed Build**
   - **Stage Name:** `build-and-test`

2. **Configure Build Stage:**
   - **Primary Code Repository:** Select `bharatmart-app`
   - **Build Spec File Path:** `build_spec.yaml` (we'll create this)
   - **Build Runner:** Choose appropriate runner (e.g., `OL7_X86_64_STANDARD_10`)
   - Click **Add**

3. **Create Build Spec File:**

   Create `build_spec.yaml` in your repository:
   ```yaml
   version: 0.1
   component: build
   timeoutInSeconds: 6000
   shell: bash
   
   env:
     exportedVariables:
       - APP_VERSION
       - BUILD_NUMBER
   
   steps:
     - type: Command
       name: "Install Dependencies"
       command: |
         echo "Installing dependencies..."
         npm install
       
     - type: Command
       name: "Run Tests"
       command: |
         echo "Running tests..."
         npm test
       
     - type: Command
       name: "Build Application"
       command: |
         echo "Building application..."
         npm run build
         export APP_VERSION=$(node -p "require('./package.json').version")
         export BUILD_NUMBER=$OCI_BUILD_RUN_ID
       
     - type: Command
       name: "Create Artifact"
       command: |
         echo "Creating artifact..."
         tar -czf bharatmart-${APP_VERSION}-${BUILD_NUMBER}.tar.gz \
           dist/ \
           package.json \
           server/
       
     - type: Command
       name: "Push to Artifact Repository"
       command: |
         echo "Pushing artifact..."
         oci artifacts generic artifact put-by-path \
           --repository-id ${OCI_ARTIFACT_REPOSITORY_ID} \
           --artifact-path "bharatmart-${APP_VERSION}-${BUILD_NUMBER}.tar.gz" \
           --file-path "bharatmart-${APP_VERSION}-${BUILD_NUMBER}.tar.gz"
   
   outputArtifacts:
     - name: bharatmart-artifact
       type: GENERIC_ARTIFACT
       location: bharatmart-${APP_VERSION}-${BUILD_NUMBER}.tar.gz
   ```

4. **Commit Build Spec:**
   ```bash
   git add build_spec.yaml
   git commit -m "Add build specification"
   git push
   ```

#### Step 3: Test Build Pipeline

1. **Run Build Manually:**
   - Go to **Build Pipelines**
   - Click on `bharatmart-build-pipeline`
   - Click **Start Manual Run**
   - Select branch (e.g., `main`)
   - Click **Start**

2. **Monitor Build:**
   - Watch build progress in real-time
   - Check logs for each stage
   - Verify artifact is created

---

## 5. Hands-On Task 3 — Add Reliability Gates

#### Purpose

Add pre-deployment and post-deployment reliability gates.

### Steps:

#### Step 1: Create Pre-Deployment Gate Function

1. **Create OCI Function for Gate Checks:**

   Create function `pre-deployment-gate.py`:
   ```python
   import io
   import json
   import oci
   import logging
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   def handler(ctx, data: io.BytesIO = None):
       """
       Pre-deployment reliability gate
       Checks error budget and service health before deployment
       """
       try:
           config = {}
           
           # Get input parameters
           if data:
               params = json.loads(data.read().decode('utf-8'))
           else:
               params = ctx
           
           compartment_id = params.get('compartment_id')
           service_name = params.get('service_name', 'BharatMart')
           
           logger.info(f"Pre-deployment gate check for {service_name}")
           
           # Create Monitoring client
           monitoring = oci.monitoring.MonitoringClient(config)
           
           # Check 1: Error Budget Check
           # Query error rate for last 24 hours
           # (Simplified - in production, calculate actual error budget)
           logger.info("Checking error budget...")
           
           # Check 2: Service Health Check
           # Query current error rate and latency
           logger.info("Checking service health...")
           
           # Example: Check if error rate is acceptable
           # If error rate > 1%, block deployment
           current_error_rate = 0.5  # Example: query actual metrics
           
           if current_error_rate > 1.0:
               return {
                   "status": "BLOCKED",
                   "reason": f"Error rate too high: {current_error_rate}%",
                   "error_budget_check": "FAIL",
                   "health_check": "FAIL"
               }
           
           # Check 3: Alarms Status
           # Verify no critical alarms are firing
           logger.info("Checking alarm status...")
           
           return {
               "status": "APPROVED",
               "reason": "All checks passed",
               "error_budget_check": "PASS",
               "health_check": "PASS",
               "alarm_check": "PASS"
           }
           
       except Exception as e:
           logger.error(f"Gate check failed: {e}")
           return {
               "status": "ERROR",
               "reason": str(e)
           }
   ```

2. **Deploy Function:**
   - Create function application: `devops-gates`
   - Deploy function: `pre-deployment-gate`
   - Note function OCID for pipeline configuration

#### Step 2: Add Gate Stage to Deployment Pipeline

1. **Create Deployment Pipeline:**
   - Go to **Deployment Pipelines**
   - Click **Create Deployment Pipeline**
   - **Name:** `bharatmart-deploy-pipeline`

2. **Add Pre-Deployment Gate Stage:**
   - Click **Add Stage**
   - Select **Invoke Function**
   - **Stage Name:** `pre-deployment-gate`
   - **Function:** Select `pre-deployment-gate` function
   - **Function Parameters:**
     ```json
     {
       "compartment_id": "<compartment-ocid>",
       "service_name": "BharatMart"
     }
     ```
   - **Fail on Error:** Yes
   - Click **Add**

3. **Add Deployment Stage:**
   - Click **Add Stage**
   - Select **Compute Instance Group Deployment**
   - **Stage Name:** `deploy-to-compute`
   - Configure deployment to your Compute instances
   - Click **Add**

#### Step 3: Create Post-Deployment Validation

1. **Create Post-Deployment Gate Function:**

   Create function `post-deployment-validation.py`:
   ```python
   import io
   import json
   import oci
   import time
   import logging
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   def handler(ctx, data: io.BytesIO = None):
       """
       Post-deployment validation
       Checks health, error rate, and latency after deployment
       """
       try:
           config = {}
           
           if data:
               params = json.loads(data.read().decode('utf-8'))
           else:
               params = ctx
           
           health_endpoint = params.get('health_endpoint', 'http://<lb-ip>/api/health')
           max_wait_time = int(params.get('max_wait_time', 300))  # 5 minutes
           
           logger.info(f"Post-deployment validation: {health_endpoint}")
           
           # Wait for deployment to stabilize
           time.sleep(30)
           
           # Check 1: Health Endpoint
           import requests
           try:
               response = requests.get(health_endpoint, timeout=10)
               if response.status_code != 200:
                   return {
                       "status": "FAILED",
                       "reason": f"Health check failed: {response.status_code}"
                   }
           except Exception as e:
               return {
                   "status": "FAILED",
                   "reason": f"Health check error: {e}"
               }
           
           # Check 2: Error Rate (query metrics)
           # In production, query OCI Monitoring for actual error rate
           logger.info("Checking error rate...")
           
           # Check 3: Latency (query metrics)
           # In production, query OCI Monitoring for latency
           logger.info("Checking latency...")
           
           # Validation passed
           return {
               "status": "PASSED",
               "health_check": "PASS",
               "error_rate_check": "PASS",
               "latency_check": "PASS"
           }
           
       except Exception as e:
           logger.error(f"Validation failed: {e}")
           return {
               "status": "FAILED",
               "reason": str(e)
           }
   ```

2. **Add Post-Deployment Stage:**
   - In deployment pipeline, add **Invoke Function** stage
   - **Stage Name:** `post-deployment-validation`
   - **Function:** Select `post-deployment-validation` function
   - **Fail on Error:** Yes
   - Add after deployment stage

---

## 6. Hands-On Task 4 — Configure Pipeline Triggers

#### Purpose

Set up automatic pipeline execution on code changes.

### Steps:

#### Step 1: Create Build Trigger

1. **Navigate to Triggers:**
   - In DevOps project, go to **Triggers**
   - Click **Create Trigger**

2. **Configure Build Trigger:**
   - **Name:** `bharatmart-build-trigger`
   - **Trigger Source:** Code Repository
   - **Repository:** Select `bharatmart-app`
   - **Events:** Push to branch
   - **Branch:** `main` (or your main branch)
   - **Build Pipeline:** Select `bharatmart-build-pipeline`
   - Click **Create**

#### Step 2: Create Deployment Trigger

1. **Create Deployment Trigger:**
   - Click **Create Trigger**
   - **Name:** `bharatmart-deploy-trigger`
   - **Trigger Source:** Artifact
   - **Artifact:** Select artifact from build pipeline
   - **Deployment Pipeline:** Select `bharatmart-deploy-pipeline`
   - Click **Create**

#### Step 3: Test Trigger

1. **Make Code Change:**
   ```bash
   # Make a small change
   echo "# Test trigger" >> README.md
   git add README.md
   git commit -m "Test pipeline trigger"
   git push
   ```

2. **Verify Pipeline Execution:**
   - Go to **Build Pipelines**
   - Verify build pipeline started automatically
   - Monitor build progress

---

## 7. Hands-On Task 5 — Integrate SLI Validation

#### Purpose

Add explicit SLI validation to deployment pipeline.

### Steps:

#### Step 1: Create SLI Validation Script

1. **Create SLI Validation Function:**

   Create function `sli-validation.py`:
   ```python
   import io
   import json
   import oci
   import logging
   from datetime import datetime, timedelta
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   def handler(ctx, data: io.BytesIO = None):
       """
       SLI validation for deployment
       Validates SLIs meet SLO targets
       """
       try:
           config = {}
           
           if data:
               params = json.loads(data.read().decode('utf-8'))
           else:
               params = ctx
           
           compartment_id = params.get('compartment_id')
           slo_targets = params.get('slo_targets', {
               'availability': 99.9,
               'latency_p95': 500,  # milliseconds
               'error_rate': 0.1  # percentage
           })
           
           logger.info("Validating SLIs against SLOs...")
           
           # Create Monitoring client
           monitoring = oci.monitoring.MonitoringClient(config)
           
           end_time = datetime.now()
           start_time = end_time - timedelta(hours=1)
           
           results = {}
           
           # SLI 1: Availability
           # Query uptime/health metrics
           # Calculate availability percentage
           # Compare with SLO target
           
           # SLI 2: Latency
           # Query latency metrics (P95)
           latency_p95 = 250  # Example: query actual metric
           results['latency'] = {
               'value': latency_p95,
               'target': slo_targets['latency_p95'],
               'pass': latency_p95 < slo_targets['latency_p95']
           }
           
           # SLI 3: Error Rate
           # Query error rate metrics
           error_rate = 0.05  # Example: query actual metric
           results['error_rate'] = {
               'value': error_rate,
               'target': slo_targets['error_rate'],
               'pass': error_rate < slo_targets['error_rate']
           }
           
           # Determine overall status
           all_pass = all(r['pass'] for r in results.values())
           
           return {
               "status": "PASSED" if all_pass else "FAILED",
               "sli_results": results,
               "timestamp": datetime.now().isoformat()
           }
           
       except Exception as e:
           logger.error(f"SLI validation failed: {e}")
           return {
               "status": "ERROR",
               "reason": str(e)
           }
   ```

2. **Add SLI Validation Stage:**
   - Add to deployment pipeline as post-deployment stage
   - Configure with SLO targets
   - Set to fail pipeline if SLIs don't meet targets

---

## 8. Summary of the Hands-On

In this exercise, you:

* Created OCI DevOps project and repositories
* Built CI/CD pipeline with build stages
* Added reliability gates (pre and post-deployment)
* Configured pipeline triggers
* Integrated SLI validation into deployment
* Implemented SRE practices in CI/CD workflow

This demonstrates how SRE principles integrate into DevOps pipelines for reliable deployments.

---

## 9. Best Practices

### Reliability Gates:

* **Always check error budget** before deployment
* **Validate service health** before and after deployment
* **Monitor metrics** during deployment window
* **Automatic rollback** on SLO breach
* **Gradual rollout** (canary deployments) when possible

### SLI Integration:

* **Define clear SLIs** before creating gates
* **Set appropriate thresholds** for validation
* **Monitor trends** not just point-in-time values
* **Document SLO targets** in pipeline configuration
* **Review and adjust** thresholds based on historical data

---

## 10. Troubleshooting

### Build Pipeline Fails

* Check build logs for errors
* Verify build_spec.yaml syntax
* Ensure dependencies are available
* Check artifact repository permissions

### Deployment Blocked by Gate

* Review gate function logs
* Check error budget status
* Verify service health
* Review alarm status

### SLI Validation Fails

* Check current SLI values vs targets
* Review metric queries in validation function
* Verify SLO targets are realistic
* Consider adjusting thresholds if needed

---

## 11. Solutions Key (Instructor Reference)

### ✔ Solution Key — Task 1: DevOps Project

#### Expected Configuration:

* Project: `<student-id>-bharatmart-devops`
* Repository: `bharatmart-app` (connected or created)
* Artifact Repository: `bharatmart-artifacts`

### ✔ Solution Key — Task 2: Build Pipeline

#### Expected Results:

* Build pipeline created
* Build stages execute successfully
* Artifacts created and stored

### ✔ Solution Key — Task 3: Reliability Gates

#### Expected Results:

* Pre-deployment gate function created
* Post-deployment validation function created
* Gates integrated into deployment pipeline

### ✔ Solution Key — Task 4: Triggers

#### Expected Results:

* Build trigger fires on code push
* Deployment trigger fires on artifact creation
* Pipelines execute automatically

---

## End of Hands-On Document
