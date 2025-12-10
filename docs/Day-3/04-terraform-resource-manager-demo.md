# Day 3: Automate Compute Instance Provisioning using OCI Resource Manager (Terraform) - Demonstration

### Audience Context: IT Engineers and Developers

---
## 1. Purpose

Demonstrate how to automate infrastructure provisioning using OCI Resource Manager with Terraform, showing how automation eliminates manual toil in infrastructure operations.

---

## 2. Prerequisites
* Terraform template prepared (BharatMart infrastructure template)

---

## 3. What to Demonstrate

1. **Infrastructure as Code Concepts**
   * Benefits of IaC for toil reduction
   * Terraform as infrastructure definition language
   * OCI Resource Manager as managed Terraform execution platform

2. **Terraform Template Structure**
   * Variables for configuration
   * Resource definitions
   * Outputs for created resources

3. **Resource Manager Workflow**
   * Creating a stack from Terraform template
   * Planning infrastructure changes
   * Applying infrastructure changes
   * Reviewing created resources

4. **Toil Reduction Demonstration**
   * Compare manual provisioning (hours) vs automated (minutes)
   * Show consistency across multiple deployments
   * Demonstrate error reduction through automation

---

## 4. Demonstration Steps

#### Step 1: Show Manual Provisioning Time (Optional Comparison)

Demonstrate or describe how long manual provisioning takes:

* VCN creation: ~15-20 minutes
* Subnet configuration: ~10 minutes
* Security list setup: ~15 minutes
* Compute instance provisioning: ~10 minutes
* Load Balancer setup: ~15-20 minutes
* **Total: ~65-85 minutes** with high risk of errors

---

#### Step 2: Access OCI Resource Manager

1. Navigate to **OCI Console** → Click **Menu (☰)** in top-left → **Developer Services** → **Resource Manager** → **Stacks**
2. Click **Create Stack**

---

#### Step 3: Upload Terraform Configuration

1. Select **Zip file** as configuration source
2. Upload prepared Terraform zip file
3. Click **Next**

---

#### Step 4: Configure Stack Variables

1. **Stack Information:**
   - Name: `bharatmart-infrastructure-automation-demo`
   - Description: `BharatMart infrastructure for Day 3 automation demonstration`
   - Compartment: Select appropriate compartment

2. **Variables Configuration:**
   - `compartment_id`: Select compartment for resources
   - `region`: Select region (e.g., `us-ashburn-1`)
   - `instance_count`: Set to `2` (for demonstration)
   - `instance_shape`: `VM.Standard.E2.1`
   - `ssh_public_key`: Provide SSH public key for access
   - Other variables as needed

3. Click **Next**

---

#### Step 5: Review and Create Stack

1. Review configuration summary
2. Enable **Terraform Version:** Select version (e.g., 1.5.0 or later)
3. Click **Create**

---

#### Step 6: Run Terraform Plan

1. Once stack is created, click **Plan** button
2. Review plan job output:
   - Resources to be created (VCN, Subnets, Compute instances, Load Balancer)
   - Estimated costs
   - Configuration validation

3. **Key Resources Being Created:**
   - VCN with public and private subnets
   - Internet Gateway and NAT Gateway
   - Security Lists with appropriate rules
   - 2 Compute instances for BharatMart backend
   - Load Balancer with health checks configured on `/api/health` endpoint

4. **Emphasize:** This plan would take hours to create manually, but Terraform generates it in seconds.

---

#### Step 7: Apply Infrastructure

1. Click **Apply** button
2. Monitor apply job progress
3. Review outputs:
   - Load Balancer IP address
   - Compute instance OCIDs
   - VCN and subnet OCIDs

4. **Timing:** Note the total time (typically 10-15 minutes for complete infrastructure)

---

#### Step 8: Verify Created Resources

1. Navigate to **Compute** → **Instances**:
   - Verify 2 instances are running
   - Check instance names and shapes

2. Navigate to **Networking** → **Load Balancers**:
   - Verify Load Balancer is active
   - Review backend set configuration
   - Check health check endpoint: `/api/health`

3. Navigate to **Networking** → **Virtual Cloud Networks**:
   - Verify VCN and subnets are created
   - Review security list rules

---

#### Step 9: Demonstrate Repeatability (Optional)

Show that the same stack can be used to create identical infrastructure in a different compartment or region:

1. Create a new stack with same Terraform template
2. Change compartment_id variable
3. Show that infrastructure is identical in structure

---

## 5. Key Points to Emphasize

#### Time Savings:

* Manual provisioning: 65-85 minutes
* Automated provisioning: 10-15 minutes
* **75-85% time reduction**

#### Error Reduction:

* Manual operations: High error rate (wrong subnets, missing security rules, configuration drift)
* Automated operations: Consistent, error-free deployments

#### Consistency:

* Same template produces identical infrastructure every time
* No configuration drift between environments

#### Toil Elimination:

* Eliminates repetitive manual provisioning tasks
* Frees up engineering time for valuable work
* Enables self-service infrastructure provisioning

#### SRE Benefits:

* Infrastructure as Code enables disaster recovery
* Version-controlled infrastructure changes
* Automated infrastructure testing and validation

---

## 6. What Should Observe

* How Terraform templates define infrastructure declaratively
* The workflow from template upload to resource creation
* How variables enable configuration flexibility
* Resource Manager's role in managing Terraform execution
* Time savings compared to manual provisioning
* Consistency of automated deployments

---

