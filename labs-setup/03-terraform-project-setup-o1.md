# 🚀 **OCI Terraform Deployment Runbook**

**Environment:** Ubuntu 24.04
**Components:** VCN, Subnets, IGW, NAT, LB, Compute (Public IP + SSH)

---

# =========================================================

# **1. Prerequisites (Verify First)**

# =========================================================

### **Check OCI CLI:**

```bash
oci iam region list
```

### **Check Terraform:**

```bash
terraform --version
```

---

# =========================================================

# **2. Discover Required Terraform Variable Values (OCI CLI)**

# =========================================================

### **2.1 Get Compartment OCID**

```bash
oci iam compartment list --all \
  --query "data[].{name:name, id:id}" --output table
```

Pick your compartment, or filter:

```bash
oci iam compartment list --all \
  --query "data[?name=='sre-lab-compartment'].id | [0]" --raw-output
```

Store it:

```bash
COMPARTMENT_ID="<OCID>"
```

---

### **2.2 Get Compatible Oracle Linux Image ID**

```bash
oci compute image list \
  --compartment-id $COMPARTMENT_ID \
  --operating-system "Oracle Linux" \
  --operating-system-version "8" \
  --query "data[].{name:\"display-name\", id:id}" --output table
```

Pick **ARM image**, then:

```bash
IMAGE_ID="ocid1.image.oc1.ap-mumbai-1.aaaaaaaauolbgcffeswcqoyxezsv6d56gx5veqwutnlzplqqhqpdrtiv4k2a"
```

Confirm:

```bash
oci compute image get --image-id $IMAGE_ID
```

---

### **2.3 Get Compatible Compute Shapes for the Image**

```bash
oci compute image-shape-compatibility-entry list \
  --image-id $IMAGE_ID \
  --query "data[].shape" --raw-output | sort -u
```

Choose one (example):

```
VM.Standard.A1.Flex
```

Set:

```bash
SHAPE="VM.Standard.A1.Flex"
```

---

### **2.4 Get Availability Domains**

```bash
oci iam availability-domain list \
  --compartment-id $COMPARTMENT_ID \
  --query "data[].name" --raw-output
```

---

### **2.5 Get SSH public key**

```bash
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub
```

Copy the full string into terraform.tfvars.

---

# =========================================================

# **3. Update terraform.tfvars**

# =========================================================

Example:

```hcl
compartment_id       = "<COMPARTMENT_OCID>"
image_id             = "<IMAGE_OCID>"
ssh_public_key       = "ssh-rsa AAAA..."
compute_instance_shape = "VM.Standard.A1.Flex"
region               = "ap-mumbai-1"
project_name         = "bharatmart"
environment          = "dev"
```

---

# =========================================================

# **4. Move to Terraform Directory**

# =========================================================

```bash
cd ~/oci-multi-tier-web-app-ecommerce/deployment/terraform/option-1
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

# **7. Review Deployment Plan**

# =========================================================

```bash
terraform plan
```

---

# =========================================================

# **8. Deploy Infrastructure**

# =========================================================

```bash
terraform apply
```

Approve:

```
yes
```

Resources created:

✔ VCN
✔ Public Subnet (for VM with public IP)
✔ Private Subnet
✔ IGW, NAT
✔ Load Balancer
✔ Compute instance with SSH access

---

# =========================================================

# **9. Retrieve Outputs**

# =========================================================

```bash
terraform output
```

Specifically:

```bash
terraform output -raw compute_instance_public_ip
terraform output -raw load_balancer_url
```

---

# =========================================================

# **10. SSH into Your Instance**

# =========================================================

```bash
ssh -i ~/.ssh/id_rsa opc@$(terraform output -raw compute_instance_public_ip)
```

---

# =========================================================

# **11. Destroy Infrastructure (Optional)**

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

# **12. Troubleshooting (Quick Checks)**

# =========================================================

### **401 Authentication issues**

Use unencrypted key:

```bash
key_file=/home/adminuser/.oci/oci_api_key_unencrypted.pem
```

### **Shape invalid**

List compatible shapes:

```bash
oci compute image-shape-compatibility-entry list --image-id $IMAGE_ID
```

### **SSH not working**

Ensure port 22 is allowed:

```hcl
ingress_security_rules {
  protocol = "6"
  source   = "0.0.0.0/0"
  tcp_options { min = 22, max = 22 }
}
```

### **No public IP**

Ensure:

```hcl
assign_public_ip = true
subnet_id        = oci_core_subnet.public_subnet.id
```

### Deployment Diagram
```
                           +-----------------------------+
                           |      OCI Region: Mumbai     |
                           +-----------------------------+
                                      |
                                      |
                           +-----------------------------+
                           |     Virtual Cloud Network    |
                           |        CIDR: 10.0.0.0/16     |
                           +-----------------------------+
                                      |
       -------------------------------------------------------------------
       |                                                                 |
       |                                                                 |
+-----------------------+                                   +-----------------------+
|  Public Subnet        |                                   |   Private Subnet      |
|  CIDR: 10.0.1.0/24     |                                   |   CIDR: 10.0.2.0/24    |
|  Route Table → IGW     |                                   |   Route Table → NAT    |
|  Security List:        |                                   |   Security List:       |
|   - Allow 80/443/22    |                                   |    - Allow LB → 3000   |
+-----------------------+                                   +-----------------------+
        |                                                                  |
        |                                                                  |
        |                                                                  |
+-----------------------+                                   +-----------------------+
| Public Load Balancer  |                                   |  (Future) DB Tier     |
| Shape: Flexible        |                                   |  MySQL / ATP          |
| IP: <public-lb-ip>     |                                   |                       |
| Listener: 80 → BS      |                                   +-----------------------+
| Backend Set: 3000      |
+-----------+-----------+
            |
            | (Health-checked traffic on port 3000)
            |
+-----------------------+
| Backend Compute VM    |
| Shape: VM.Standard.A1.Flex
| Public IP: <vm-public-ip>
| Private IP: 10.0.2.x  |
| SSH allowed (22)       |
| App listens on :3000   |
+-----------------------+
            |
            |
     +-------------+
     | NAT Gateway |
     +-------------+
            |
            |
     +-------------+
     | Internet GW |
     +-------------+
```