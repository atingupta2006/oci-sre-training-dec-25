# Day 1: Create a Multi-Region OCI Tenancy (Demonstration)

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

This is an instructor-led demonstration. Students observe the setup process.

**Assumed Context:**

* **Instructor** has OCI tenancy with admin access
* **Multiple regions** available in the tenancy
* **Purpose:** Demonstrate multi-region configuration for high availability

---

## 1. Purpose

Demonstrate how to configure an OCI tenancy to support multi-region deployments, which is essential for high availability and disaster recovery scenarios.

---

## 2. Prerequisites

* OCI tenancy with admin access
* Understanding of OCI regions and availability domains

---

## 3. What You'll Demonstrate

1. **Region Selection Strategy**
   * Selecting primary and secondary regions
   * Considerations for latency, compliance, and data residency

2. **Multi-Region Tenancy Configuration**
   * Enabling multiple regions in OCI console
   * Configuring compartments for multi-region organization
   * Setting up region-specific naming conventions

3. **Network Configuration for Multi-Region**
   * Understanding VCN isolation across regions
   * Planning for cross-region connectivity (if needed)
   * Security list considerations

---

## 4. Demonstration Steps

#### Step 1: Access OCI Console and Region Selection

1. Navigate to **OCI Console** → Click **Menu (☰)** in top-left → **Governance & Administration** → **Tenancy Details**
2. In the **Tenancy Details** page, review available regions listed in the **Region Subscriptions** section
3. Select two regions for demonstration:
   - **Primary Region:** `us-ashburn-1` (example)
   - **Secondary Region:** `us-phoenix-1` (example)

#### Step 2: Enable Multi-Region Access

1. Go to **Menu (☰)** → **Governance & Administration** → **Region Management** (or from Tenancy Details, click **Manage Region Subscriptions**)
2. Review **Region Subscriptions** tab to see available regions
3. If secondary region is not subscribed, click **Subscribe to Region** and select the region
4. Verify region status shows as **Active** and accessible

#### Step 3: Create Compartments for Multi-Region Organization

1. Navigate to **Menu (☰)** → **Identity & Security** → **Domains** → **Default Domain** → **Compartments** (or **Menu (☰)** → **Identity & Security** → **Compartments**)
2. Click **Create Compartment**
3. Create compartment structure:
   * `prod-primary` (for primary region resources)
   * `prod-secondary` (for secondary region resources)
   * `shared-services` (for resources shared across regions)

#### Step 4: Demonstrate Multi-Region VCN Setup

1. **In Primary Region:**

   * Switch to primary region using the **Region** selector in top-right of OCI Console
   * Navigate to **Menu (☰)** → **Networking** → **Virtual Cloud Networks**
   * Show VCN creation in primary region
   * Note VCN name: `bharatmart-prod-primary-vcn`

2. **In Secondary Region:**

   * Switch region using **Region** selector in top-right of OCI Console
   * Navigate to **Menu (☰)** → **Networking** → **Virtual Cloud Networks**
   * Show VCN creation in secondary region
   * Note VCN name: `bharatmart-prod-secondary-vcn`

---

## 5. Key Points to Emphasize

#### Multi-region benefits:

* Disaster recovery capability
* Geographic redundancy
* Compliance with data residency requirements

#### Challenges:

* Data synchronization between regions
* Latency considerations for cross-region communication
* Increased complexity in management

#### SRE Considerations:

* Monitoring across regions
* Incident response procedures for region failures
* Capacity planning per region

---

## 6. What Students Should Observe

* How regions are organized and accessed in OCI console
* Compartment strategy for multi-region deployments
* VCN isolation between regions
* Region switching in OCI console

