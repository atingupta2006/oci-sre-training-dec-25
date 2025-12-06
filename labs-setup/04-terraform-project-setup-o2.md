Here is your **fully updated, clean, minimal, and accurate Terraform Deployment Runbook**, **rewritten to match your NEW infrastructure**, which now includes:

✔ **Frontend VM Tier + Frontend LB**
✔ **Backend VM Tier + Backend LB**
✔ **Optional backend public IP**
✔ **All updated OCI CLI discovery commands**
✔ **Updated diagram**
✔ **Updated outputs & variables**
✔ **Simplified, production-ready workflow**

Everything is aligned with the **latest Terraform architecture** we designed.

---

# 🚀 **OCI Terraform Deployment Runbook – Updated for Frontend + Backend Architecture**

**Environment:** Ubuntu 24.04
**Infra Components:** VCN, Subnets, IGW, NAT, Public LB, Private LB, Frontend VM, Backend VM, SSH, Optional Public IP

---

# =========================================================

# **1. Prerequisites**

# =========================================================

### ✔ Validate OCI CLI

```bash
oci iam region list
```

### ✔ Validate Terraform

```bash
terraform --version
```

---

# =========================================================

# **2. Discover Required Terraform Variables (OCI CLI)**

# =========================================================

## **2.1 Get Compartment OCID**

```bash
oci iam compartment list --all \
  --query "data[].{name:name, id:id}" --output table
```

Filter by name:

```bash
oci iam compartment list --all \
  --query "data[?name=='sre-lab-compartment'].id | [0]" --raw-output
```

Set variable:

```bash
COMPARTMENT_ID="<ocid>"
```

---

## **2.2 Get Oracle Linux Image ID (ARM / A1 Flex)**

```bash
oci compute image list \
  --compartment-id $COMPARTMENT_ID \
  --operating-system "Oracle Linux" \
  --operating-system-version "8" \
  --query "data[].{name:\"display-name\", id:id}" --output table
```

Pick ARM image and save:

```bash
IMAGE_ID="ocid1.image.oc1.ap-mumbai-1.xxxxx"
```

Confirm:

```bash
oci compute image get --image-id $IMAGE_ID
```

---

## **2.3 Get Supported Shapes for This Image**

```bash
oci compute image-shape-compatibility-entry list \
  --image-id $IMAGE_ID \
  --query "data[].shape" --raw-output | sort -u
```

Use recommended:

```
VM.Standard.A1.Flex
```

---

## **2.4 Get Availability Domains**

```bash
oci iam availability-domain list \
  --compartment-id $COMPARTMENT_ID \
  --query "data[].name" --raw-output
```

---

## **2.5 Get Your SSH Public Key**

```bash
cat ~/.ssh/id_rsa.pub
```

Copy to terraform.tfvars.

---

# =========================================================

# **3. Update terraform.tfvars**

# =========================================================

Your file should now include:

```hcl
compartment_id = "<OCID>"
image_id       = "<IMAGE_ID>"
ssh_public_key = "ssh-rsa AAAA..."
compute_instance_shape = "VM.Standard.A1.Flex"

# New variables
backend_public_ip = false
frontend_instance_count = 1
backend_instance_count  = 1
```

---

# =========================================================

# **4. Move to Terraform Directory**

# =========================================================

```bash
cd ~/oci-multi-tier-web-app-ecommerce/deployment/terraform
```

---

# =========================================================

# **5. Format + Validate**

# =========================================================

```bash
terraform fmt
terraform validate
```

---

# =========================================================

# **6. Initialize Terraform**

# =========================================================

```bash
terraform init
```

---

# =========================================================

# **7. Review Terraform Plan**

# =========================================================

```bash
terraform plan
```

You should see:

* VCN
* Public Subnet (frontend + LB)
* Private Subnet (backend + LB)
* IGW / NAT
* Frontend LB → Frontend VM(s)
* Backend LB → Backend VM(s)
* Optional backend public IP

---

# =========================================================

# **8. Apply Deployment**

# =========================================================

```bash
terraform apply
```

Approve:

```
yes
```

---

# =========================================================

# **9. Retrieve Outputs**

# =========================================================

```bash
terraform output
```

Common outputs:

```bash
terraform output -raw frontend_lb_url
terraform output -raw backend_lb_private_url
terraform output -raw frontend_public_ips
terraform output -raw backend_private_ips
```

If backend public IP enabled:

```bash
terraform output -raw backend_public_ips
```

---

# =========================================================

# **10. SSH Access**

# =========================================================

### Frontend VM (public IP)

```bash
ssh -i ~/.ssh/id_rsa opc@$(terraform output -raw frontend_public_ips)
```

### Backend VM (if backend_public_ip=true)

```bash
ssh -i ~/.ssh/id_rsa opc@$(terraform output -raw backend_public_ips)
```

Otherwise you need VPN/Bastion.

---

# =========================================================

# **11. Destroy Infrastructure**

# =========================================================

```bash
terraform destroy
```

Approve:

```
yes
```

---

# =========================================================

# **12. Troubleshooting**

# =========================================================

### ❌ 401 Authentication Errors

Use UNENCRYPTED OCI API key:

```
~/.oci/oci_api_key_unencrypted.pem
```

### ❌ Shape Not Valid

```bash
oci compute image-shape-compatibility-entry list --image-id $IMAGE_ID
```

### ❌ SSH Not Working

Ensure public subnet allows inbound 22:

```hcl
ingress_security_rules {
  protocol = "6"
  source = "0.0.0.0/0"
  tcp_options { min = 22, max = 22 }
}
```

### ❌ Backend not reachable

Backend runs behind private LB → **no direct public access** unless enabled.

---

# =========================================================

# **13. Updated Deployment Diagram (Frontend + Backend + Dual LB)**

# =========================================================

```
                            +-----------------------------+
                            |      OCI Region: Mumbai     |
                            +-----------------------------+
                                        |
                                        |
                       +----------------------------------------+
                       |      Virtual Cloud Network (VCN)        |
                       |             10.0.0.0/16                 |
                       +----------------------------------------+
                     /                                            \
                    /                                              \
+--------------------------------+          +--------------------------------+
|        Public Subnet          |          |        Private Subnet          |
|        10.0.1.0/24            |          |        10.0.2.0/24             |
+--------------------------------+          +--------------------------------+
          |      |                                  |        |
          |      |                                  |        |
+-----------------------------+       +-------------------------------+
| Frontend Load Balancer      |       | Backend Load Balancer (Private) |
| Listener: 80                |       | Listener: 3000                  |
+-------------+---------------+       +-------------+------------------+
              |                                 |
     +--------+--------+          +--------------+--------------+
     | Frontend VM(s) |          |         Backend VM(s)        |
     | React/Angular  |          | Node.js API (port 3000)      |
     | Public IP(s)   |          | Private IP(s), NAT outbound   |
     +----------------+          +-------------------------------+
              |                                 |
              |                                 |
     +--------------+                 +----------------+
     | Internet GW  |                 | NAT Gateway    |
     +--------------+                 +----------------+
```

---

# ✅ **Runbook Updated — Fully aligned with your new Terraform architecture**

If you want, I can also:

✅ Convert this to **PDF**, **Markdown README**, or **Confluence version**
✅ Generate a **draw.io (XML) diagram**
✅ Create **Terraform modules** for frontend/backend/network
✅ Add **Autonomous DB / Redis / Object Storage**

Would you like any of those?
