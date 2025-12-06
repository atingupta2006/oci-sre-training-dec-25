# Day 1: Set up Identity Domains and IAM Policies for SRE Access Control (Hands-on Lab)

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will create IAM policies on your OCI tenancy.

**Prerequisites:**

* OCI tenancy with admin access (or user with IAM policy management permissions)
* Understanding of IAM concepts (compartments, policies, groups, users)

---

## 1. Purpose

IAM (Identity and Access Management) policies control who can access which OCI resources. This lab shows you how to create IAM policies that grant appropriate access for SRE tasks while following the principle of least privilege.

---

## 2. Steps

#### Step 1: Create an SRE Group

1. Navigate to **Menu (☰)** → **Identity & Security** → **Domains** → **Default Domain**
2. Click **Groups** in the left navigation
3. Click **Create Group**
4. **Fill in the form:**

   * **Name:** `sre-engineers`
   * **Description:** `Site Reliability Engineers with monitoring and operational access`

5. Click **Create**

#### Step 2: Create IAM Policy for SRE Monitoring Access

1. Navigate to **Menu (☰)** → **Identity & Security** → **Policies**
2. Select your tenancy or appropriate compartment from the compartment dropdown
3. Click **Create Policy**

4. **Fill in Policy Information:**

   * **Name:** `sre-monitoring-policy`
   * **Description:** `Allows SRE engineers to view monitoring metrics, alarms, and dashboards`
   * **Compartment:** Select your tenancy or root compartment

5. **Add Policy Statements:**
   ```
   Allow group sre-engineers to read metrics in tenancy
   Allow group sre-engineers to read alarms in tenancy
   Allow group sre-engineers to read dashboards in tenancy
   Allow group sre-engineers to use log-content in tenancy
   Allow group sre-engineers to read log-groups in tenancy
   Allow group sre-engineers to read log-saved-searches in tenancy
   ```

6. Click **Create**

#### Step 3: Create IAM Policy for SRE Operational Access

1. From **Identity & Security** → **Policies**, click **Create Policy** again

2. **Fill in Policy Information:**

   * **Name:** `sre-operational-policy`
   * **Description:** `Allows SRE engineers to manage compute instances, view resources, and access logs`
   * **Compartment:** Select your tenancy or root compartment

3. **Add Policy Statements:**
   ```
   Allow group sre-engineers to read instances in tenancy
   Allow group sre-engineers to manage instance-console-connections in tenancy
   Allow group sre-engineers to read load-balancers in tenancy
   Allow group sre-engineers to read virtual-network-family in tenancy
   Allow group sre-engineers to inspect work-requests in tenancy
   Allow group sre-engineers to read audit-events in tenancy
   ```

4. Click **Create**

#### Step 4: Create IAM Policy for SRE Resource Manager Access (Optional)

For SRE engineers who need to manage infrastructure via Terraform:

1. From **Identity & Security** → **Policies**, click **Create Policy** again

2. **Fill in Policy Information:**

   * **Name:** `sre-resource-manager-policy`
   * **Description:** `Allows SRE engineers to manage Resource Manager stacks for infrastructure automation`
   * **Compartment:** Select your tenancy or root compartment

3. **Add Policy Statements:**
   ```
   Allow group sre-engineers to manage orm-stacks in tenancy
   Allow group sre-engineers to manage orm-jobs in tenancy
   Allow group sre-engineers to read work-requests in tenancy
   ```

4. Click **Create**

#### Step 5: Assign Users to SRE Group

1. Navigate to **Identity & Security** → **Domains** → **Default Domain** → **Groups**
2. Click on **sre-engineers** group
3. Click **Add User to Group**
4. Select user(s) to add
5. Click **Add**

#### Step 6: Verify IAM Policies (Test Access)

If you have a test user in the `sre-engineers` group, verify access:

**Using OCI CLI in Cloud Shell:**

```bash
# Test monitoring access
oci monitoring metric list \
  --namespace oci_computeagent \
  --compartment-id <compartment-ocid>

# Test compute instance access
oci compute instance list \
  --compartment-id <compartment-ocid>

# Test load balancer access
oci lb load-balancer list \
  --compartment-id <compartment-ocid>
```

**Expected:** Successful API calls returning resource lists (or empty lists if no resources exist)

**If access denied:** Verify:

* User is in `sre-engineers` group
* Policies are created in correct compartment
* Policy statements are correct

#### Step 7: Create Compartment-Specific SRE Policy (Best Practice)

For production environments, create compartment-scoped policies:

1. Navigate to your production compartment
2. Click **Create Policy**

3. **Policy Information:**

   * **Name:** `sre-production-access`
   * **Description:** `SRE access to production compartment resources`
   * **Compartment:** Select your production compartment

4. **Policy Statements:**
   ```
   Allow group sre-engineers to read all-resources in compartment <compartment-name>
   Allow group sre-engineers to manage alarms in compartment <compartment-name>
   Allow group sre-engineers to manage dashboards in compartment <compartment-name>
   Allow group sre-engineers to use log-content in compartment <compartment-name>
   ```

5. Replace `<compartment-name>` with your compartment name

6. Click **Create**

---

## 3. What You Should See

* `sre-engineers` group created
* Three IAM policies created (monitoring, operational, resource manager)
* Users assigned to the group
* Successful API calls verifying access

---

## 4. Key IAM Policy Patterns for SRE

#### Read-Only Monitoring Access
```
Allow group sre-engineers to read metrics in tenancy
Allow group sre-engineers to read alarms in tenancy
Allow group sre-engineers to read dashboards in tenancy
```

#### Log Analysis Access
```
Allow group sre-engineers to use log-content in tenancy
Allow group sre-engineers to read log-groups in tenancy
Allow group sre-engineers to read log-saved-searches in tenancy
```

#### Operational Access (Limited Write)
```
Allow group sre-engineers to read instances in tenancy
Allow group sre-engineers to manage instance-console-connections in tenancy
Allow group sre-engineers to inspect work-requests in tenancy
```

---

## 5. Best Practices

1. **Principle of Least Privilege:** Only grant minimum permissions needed
2. **Compartment-Level Policies:** Scope policies to specific compartments when possible
3. **Group-Based Access:** Use groups instead of individual user policies
4. **Regular Reviews:** Periodically review and audit IAM policies
5. **Separate Environments:** Different policies for dev/staging/prod compartments

---

## 6. Troubleshooting

#### Access Denied Errors:

* Verify user is in the correct group
* Check policy statements are correct
* Ensure policies are in the correct compartment scope
* Verify tenancy vs compartment-level policies

#### Cannot Create Policies:

* Verify you have IAM policy management permissions
* Check you're in the correct compartment
* Ensure you're using the default domain

---

## 7. Key Takeaways

* IAM policies control access to OCI resources
* Groups simplify user management and policy assignment
* Compartment-level policies provide better security isolation
* SRE access should be read-focused with limited write permissions
* Regular policy audits ensure security compliance
* These policies will be used throughout the training for SRE operations

