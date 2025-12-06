# 🚀 **BharatMart Terraform Deployment – Oracle Cloud Infrastructure (OCI)**

This guide explains how to:

1. Fetch **all required OCI IDs** using OCI CLI
2. Configure Terraform automatically
3. Deploy the BharatMart infrastructure
4. Manage terraform.tfvars using **sed**, **cp**, and CLI automation

---

# 📦 **1. Prerequisites**

## ✔ Install OCI CLI

Linux / macOS:

```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

Verify:

```bash
oci --version
```

---

# 🔐 **2. Authenticate with OCI**

Run:

```bash
oci setup config
```

This creates:

```
~/.oci/config
```

To verify authentication:

```bash
oci iam region list
```

---

# 📥 **3. Fetch Required OCI Values for terraform.tfvars**

Below are all mandatory variables for your Terraform project and the commands to retrieve them.

---

## 🎯 **3.1 Get Tenancy OCID**

```bash
grep tenancy ~/.oci/config | awk -F'=' '{print $2}' | tr -d ' '
```

---

## 🎯 **3.2 Get User OCID**

```bash
oci iam user list --all \
  --query "data[?name=='$(whoami)'].id | [0]" \
  --raw-output
```

---

## 🎯 **3.3 Get Compartment OCID**

List all compartments:

```bash
oci iam compartment list --all \
  --query "data[].{Name:name,ID:id}" \
  --output table
```

Find the correct compartment and set:

```bash
COMPARTMENT_ID="<paste_here>"
```

---

## 🎯 **3.4 Get Latest Oracle Linux ARM Image ID**

Required for A1 Flex:

```bash
oci compute image list \
  --compartment-id $COMPARTMENT_ID \
  --all \
  --operating-system "Oracle Linux" \
  --operating-system-version "8" \
  --shape "VM.Standard.A1.Flex" \
  --query "data[0].id" --raw-output
```

---

# 🌐 **4. Prepare terraform.tfvars Automatically**

Your project contains `terraform.tfvars.example`.

## ✔ 4.1 Create terraform.tfvars

```bash
cp terraform.tfvars.example terraform.tfvars
```

---

## ✔ 4.2 Use sed to auto-fill values

### **Set Compartment ID**

```bash
sed -i "s|compartment_id = .*|compartment_id = \"$COMPARTMENT_ID\"|g" terraform.tfvars
```

### **Set Tenancy OCID**

```bash
TENANCY_OCID=$(grep tenancy ~/.oci/config | awk -F'=' '{print $2}' | tr -d ' ')
sed -i "s|tenancy_ocid = .*|tenancy_ocid = \"$TENANCY_OCID\"|g" terraform.tfvars
```

### **Set Image ID**

```bash
IMAGE_ID=$(oci compute image list \
  --compartment-id $COMPARTMENT_ID \
  --all \
  --operating-system "Oracle Linux" \
  --operating-system-version "8" \
  --shape "VM.Standard.A1.Flex" \
  --query "data[0].id" --raw-output)

sed -i "s|image_id = .*|image_id = \"$IMAGE_ID\"|g" terraform.tfvars
```

### **Set SSH Public Key**

```bash
SSH_KEY=$(cat ~/.ssh/id_rsa.pub)
sed -i "s|ssh_public_key = .*|ssh_public_key = \"$SSH_KEY\"|g" terraform.tfvars
```

---

# 🏗 **5. Deploy the Terraform Project**

## ✔ Initialize

```bash
terraform init
```

---

## ✔ Validate

```bash
terraform validate
```

---

## ✔ Plan

```bash
terraform plan -out plan.out
```

---

## ✔ Apply

```bash
terraform apply plan.out
```

Expected deployment time: **5–10 minutes**

---

# 🌐 **6. After Deployment**

Get outputs:

```bash
terraform output
```

Typical:

```
frontend_public_ips = ["132.xxx.xxx.xxx"]
backend_private_ips = ["10.0.2.10"]
load_balancer_public_ip = "129.xx.xx.xx"
```

---

# 🧹 **7. Destroy Infrastructure**

```bash
terraform destroy
```

---

# 🛠 **8. Optional: Automate Entire Setup**

Create `setup.sh`:

```bash
#!/bin/bash

cp terraform.tfvars.example terraform.tfvars

COMPARTMENT_ID="<your_compartment>"
TENANCY_OCID=$(grep tenancy ~/.oci/config | awk -F'=' '{print $2}' | tr -d ' ')
IMAGE_ID=$(oci compute image list \
  --compartment-id $COMPARTMENT_ID \
  --shape "VM.Standard.A1.Flex" \
  --operating-system "Oracle Linux" \
  --operating-system-version "8" \
  --query "data[0].id" --raw-output)

SSH_KEY=$(cat ~/.ssh/id_rsa.pub)

sed -i "s|compartment_id = .*|compartment_id = \"$COMPARTMENT_ID\"|" terraform.tfvars
sed -i "s|tenancy_ocid = .*|tenancy_ocid = \"$TENANCY_OCID\"|" terraform.tfvars
sed -i "s|image_id = .*|image_id = \"$IMAGE_ID\"|" terraform.tfvars
sed -i "s|ssh_public_key = .*|ssh_public_key = \"$SSH_KEY\"|" terraform.tfvars

terraform init
terraform apply -auto-approve
```

Make executable:

```bash
chmod +x setup.sh
```

Run:

```bash
./setup.sh
```

