# Day 4: Set up a Scalable App Using OCI Load Balancer + Auto Scaling - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will configure OCI Load Balancer with Auto Scaling for BharatMart.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* BharatMart deployed on Compute instances
* Access to OCI Console

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Deploy application behind OCI Load Balancer
* Create instance pools across Fault Domains
* Configure Auto Scaling for automatic capacity adjustment
* Verify high availability and scalability

---

## 2. Background Concepts

### 2.1 Fault Domains & Redundancy

OCI Availability Domains contain Fault Domains. High availability requires deploying instances across multiple Fault Domains.

### 2.2 Load Balancing Patterns

Load balancers improve HA by distributing traffic and detecting unhealthy instances.

### 2.3 Auto Scaling

Auto Scaling automatically adjusts capacity based on metrics (CPU, memory, request rate).

---

## 3. Hands-On Task 1 — Deploy App Behind OCI Load Balancer

#### Purpose

Place BharatMart application behind a public Load Balancer for HA.

### Steps

1. Open **Navigation Menu (☰) → Networking → Load Balancers**.
2. Click **Create Load Balancer**.
3. Choose:
   * **Name:** `<student-id>-lb`
   * **Visibility:** Public
   * **Shape:** Flexible (default)
4. Under **Networking**:
   * Select your VCN
   * Create or select a **public subnet**
5. Click **Next**.

#### Frontend Listener Configuration

* **Listener Name:** `http-listener`
* **Protocol:** HTTP
* **Port:** `80`

### Expected Result

A public load balancer is created and ready for backend attachment.

---

## 4. Hands-On Task 2 — Configure Instance Pools Across Fault Domains

#### Purpose

Provide redundancy through multiple application servers across Fault Domains.

> **📝 Note: Infrastructure as Code Option Available**
> 
> You can also deploy instance pools and auto-scaling using Terraform (Infrastructure as Code). The application repository includes complete Terraform configurations:
> - **Location:** `deployment/terraform/option-2/instance-pool-autoscaling.tf`
> - **Configuration:** Instance Configuration, Instance Pool, Auto Scaling Configuration
> - **Variables:** Configure thresholds, pool size, and scaling policies via Terraform variables
> - **Documentation:** See `deployment/terraform/option-2/README.md`
> 
> **To use Terraform approach:**
> 1. Navigate to `deployment/terraform/option-2/`
> 2. Set variables in `terraform.tfvars`:
>    - `enable_instance_pool = true`
>    - `enable_auto_scaling = true`
>    - `instance_pool_size = 2`
>    - `auto_scaling_scale_out_threshold = 70`
>    - `auto_scaling_scale_in_threshold = 30`
> 3. Run `terraform apply`
> 
> The manual steps below (using OCI Console) are recommended for learning the concepts. The Terraform approach is better for automation and repeatability.

### Steps

#### A. Create Instance Configuration

1. Go to **Compute → Instance Configurations**.
2. Click **Create Instance Configuration**.
3. Use your working training instance as a base.
4. Name it: `<student-id>-app-config`
5. Save configuration.

#### B. Create Instance Pool

1. Go to **Compute → Instance Pools**.
2. Click **Create Instance Pool**.
3. Name: `<student-id>-bharatmart-pool`
4. Use config: `<student-id>-app-config`
5. Set **Number of Instances = 2**
6. **Placement Configuration:**
   * Select **Multiple Fault Domains**
   * Distribute instances across FDs
7. Create.

### Expected Result

Instance pool created with instances across multiple Fault Domains.

---

## 5. Hands-On Task 3 — Configure Auto Scaling

#### Purpose

Enable automatic scaling based on metrics.

### Steps

1. Go to **Compute → Instance Pools**.
2. Click on your instance pool.
3. Click **Auto Scaling Configuration**.
4. Click **Create Auto Scaling Configuration**.

#### Scaling Policies

**Scale-Out Policy (CPU-based):**
* **Metric:** CPU Utilization
* **Threshold:** > 70%
* **Duration:** 5 minutes
* **Action:** Add 1 instance

**Scale-In Policy (CPU-based):**
* **Metric:** CPU Utilization
* **Threshold:** < 30%
* **Duration:** 15 minutes
* **Action:** Remove 1 instance

5. Configure policies and click **Create**.

---

## 6. Hands-On Task 4 — Attach Pools to Load Balancer

#### Purpose

Connect instance pools to Load Balancer backend set.

### Steps

1. Go to your Load Balancer.
2. Open **Backend Sets → Create Backend Set**
3. Name: `bharatmart-backend`
4. Policy: `ROUND_ROBIN`
5. **Health Check:**
   * Protocol: HTTP
   * Port: 3000
   * URL Path: `/api/health`
   * Interval: 30 seconds
6. Click **Add Backends**
7. Select instances from your instance pool
8. Port: `3000`
9. Save.

### Expected Result

Load Balancer shows healthy backends from instance pool.

---

## 7. Hands-On Task 5 — Verify High Availability

#### Purpose

Validate that system maintains availability during failures.

### Steps

1. **Test Traffic Distribution:**
   ```bash
   curl http://<lb-ip>/
   ```
   Verify responses come from different instances.

2. **Simulate Instance Failure:**
   ```bash
   # Stop one instance
   oci compute instance action --instance-id <instance-ocid> --action STOP
   ```

3. **Observe Failover:**
   * Load Balancer marks instance unhealthy
   * Traffic routed to remaining instances
   * Service continues operating

4. **Verify Auto Scaling:**
   * Generate load on instances
   * Monitor CPU utilization
   * Verify auto-scaling adds instances when CPU > 70%

---

## 8. Summary of the Hands-On

In this exercise, you:

* Deployed Load Balancer for traffic distribution
* Created instance pools across Fault Domains
* Configured Auto Scaling for automatic capacity adjustment
* Validated high availability and failover
* Tested automatic scaling behavior

These steps form the foundation of high availability and scalable architecture.

---

## 9. Solutions Key (Instructor Reference)

### Expected Configuration:

* Load Balancer: `<student-id>-lb` (Public, Active)
* Instance Pool: `<student-id>-bharatmart-pool` (Multiple FDs)
* Backend Set: `bharatmart-backend` (Health checks on `/api/health`)
* Auto Scaling: CPU-based policies (scale-out >70%, scale-in <30%)

### Expected Results:

* Traffic distributed across instances
* Failover works when instance fails
* Auto-scaling adds instances under load
* Service maintains availability

---

## End of Hands-On Document

