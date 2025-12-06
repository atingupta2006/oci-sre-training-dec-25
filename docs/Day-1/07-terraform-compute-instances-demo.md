# Day 1: Launch & Configure OCI Compute Instances using Infrastructure-as-Code (Terraform) - Demonstration

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

This is an instructor-led demonstration. Students observe the infrastructure provisioning process.

**Assumed Context:**

* **Instructor** has OCI tenancy with appropriate permissions
* **Terraform template** prepared (BharatMart infrastructure template)
* **OCI Resource Manager** access available

---

## 1. Purpose

Demonstrate how to provision OCI Compute instances and supporting infrastructure using Terraform with OCI Resource Manager, showing the Infrastructure-as-Code (IaC) approach to eliminate manual provisioning toil.

---

## 2. Prerequisites

* OCI tenancy with appropriate permissions
* Terraform template prepared (BharatMart infrastructure template)
* OCI Resource Manager access

---

## 3. What You'll Demonstrate

1. **Infrastructure-as-Code Concepts**

   * Benefits of IaC over manual provisioning
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

---

## 4. Demonstration Steps

#### Step 1: Access OCI Resource Manager

1. Navigate to **OCI Console** → Click **Menu (☰)** in top-left → **Developer Services** → **Resource Manager** → **Stacks**
2. Click **Create Stack**

#### Step 2: Upload Terraform Configuration

1. Select **Zip file** as configuration source
2. Upload prepared Terraform zip file (BharatMart infrastructure template)
3. Click **Next**

#### Step 3: Configure Stack Variables

1. **Stack Information:**

   - Name: `bharatmart-infrastructure-demo`
   - Description: `BharatMart infrastructure for Day 1 demonstration`
   - Compartment: Select appropriate compartment

2. **Variables Configuration:**

   - `compartment_id`: Select compartment for resources
   - `region`: Select region (e.g., `us-ashburn-1`)
   - `instance_count`: Set to `2` (for demonstration)
   - `instance_shape`: `VM.Standard.E2.1`
   - `ssh_public_key`: Provide SSH public key for access
   - Other variables as needed

3. Click **Next**

#### Step 4: Review and Create Stack

1. Review configuration summary
2. Enable **Terraform Version:** Select version (e.g., 1.5.0 or later)
3. Click **Create**

#### Step 5: Run Terraform Plan

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

#### Step 6: Apply Infrastructure

1. Click **Apply** button
2. Monitor apply job progress
3. Review outputs:
   - Load Balancer IP address
   - Compute instance OCIDs
   - VCN and subnet OCIDs

#### Step 7: Verify Created Resources

1. **Verify Compute Instances:**

   * Navigate to **Menu (☰)** → **Compute** → **Instances**
   * Verify 2 instances are running
   * Check instance names and shapes

2. **Verify Load Balancer:**

   * Navigate to **Menu (☰)** → **Networking** → **Load Balancers**
   * Verify Load Balancer is active
   * Review backend set configuration
   * Check health check endpoint: `/api/health`

3. **Verify VCN:**

   * Navigate to **Menu (☰)** → **Networking** → **Virtual Cloud Networks**
   * Verify VCN and subnets are created
   * Review security list rules

---

## 5. Key Points to Emphasize

#### Benefits of IaC:

* Repeatability: Same infrastructure every time
* Version control: Track infrastructure changes
* Reduced errors: Automated provisioning eliminates manual mistakes
* Documentation: Infrastructure is self-documenting

#### SRE Benefits:

* Eliminates toil from manual infrastructure provisioning
* Enables infrastructure testing and validation
* Supports disaster recovery through reproducible infrastructure
* Facilitates compliance through standardized configurations

#### OCI Resource Manager Advantages:

* Managed Terraform state storage
* Built-in access control via IAM
* Integration with OCI services (Logging, Monitoring)
* Drift detection capabilities

---

## 6. What Students Should Observe

* How Terraform templates define infrastructure
* The workflow from template upload to resource creation
* How variables enable configuration flexibility
* Resource Manager's role in managing Terraform execution
* Verification of created resources in OCI console

---

## 7. Next Steps

After this demonstration, students will:

* Understand Infrastructure-as-Code concepts
* See how Terraform automates infrastructure provisioning
* Be prepared for hands-on labs using Cloud Shell and SDKs
* Recognize the value of eliminating manual infrastructure toil

