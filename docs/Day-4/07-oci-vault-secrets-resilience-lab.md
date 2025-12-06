# Day 4: Use OCI Vault + Secrets for Configuration Resilience - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will configure OCI Vault for secure secrets management.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* Compute instance running (for secret retrieval)
* Access to OCI Console

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Create OCI Vault for secure secrets storage
* Store secrets securely (database passwords, API keys)
* Retrieve secrets from Compute instances using instance principal
* Configure IAM policies for secret access

---

## 2. Background Concepts

### 2.1 Why Secrets Management Matters

Hardcoding secrets (DB passwords, API keys) is dangerous:

* Secrets exposed in code repositories
* Difficult to rotate without redeployment
* Security breaches when secrets are compromised

**Benefits of OCI Vault:**
* Secrets stored securely, encrypted
* Rotation without code changes
* Audit logs of secret access
* IAM-controlled access

---

## 3. Hands-On Task 1 — Store Secrets in OCI Vault

#### Purpose

Store application secrets securely.

### Steps

#### A. Create a Vault

1. Open **Navigation Menu (☰) → Identity & Security → Vault**.
2. Click **Create Vault**.
3. Select:
   * **Type:** "Default Vault"
   * **Name:** `<student-id>-vault`
   * **Compartment:** your training compartment
4. Click **Create Vault**.

#### B. Create a Master Key

1. Inside your vault, open **Master Encryption Keys**.
2. Click **Create Key**.
3. Enter:
   * **Name:** `<student-id>-masterkey`
   * **Protection Mode:** "HSM" or "Software"
4. Click **Create Key**.

#### C. Create the Secret

1. Inside the Vault, open **Secrets**.
2. Click **Create Secret**.
3. Enter:
   * **Name:** `<student-id>-db-password`
   * **Description:** "DB password for BharatMart"
   * **Encryption Key:** `<student-id>-masterkey`
4. Under **Secret Contents**, enter a test value:
   ```
   SuperSecretP@ss123
   ```
5. Click **Create Secret**.

### Expected Result

A new secret created in the Vault with encrypted storage.

---

## 4. Hands-On Task 2 — Configure IAM for Secret Access

#### Purpose

Enable Compute instances to retrieve secrets securely.

### Steps

#### A. Create Dynamic Group for Your Instance

1. Go to **Identity & Security → Dynamic Groups**.
2. Click **Create Dynamic Group**.
3. Name: `<student-id>-dg`
4. Rule:
   ```
   ALL {instance.id = '<your-instance-ocid>'}
   ```
   (Find instance OCID in Compute → Instances → Instance Details)
5. Save.

#### B. Create IAM Policy to Allow Secret Retrieval

1. Open **Identity & Security → Policies**.
2. Select your compartment.
3. Create Policy:
   * **Name:** `<student-id>-vault-policy`
   * **Statement:**
     ```
     Allow dynamic-group <student-id>-dg to read secret-bundles in compartment <YOUR-COMPARTMENT>
     ```
4. Save.

---

## 5. Hands-On Task 3 — Retrieve Secret from Compute Instance

#### Purpose

Retrieve secret programmatically using instance principal.

### Steps

1. **SSH into your instance:**
   ```bash
   ssh opc@<instance-public-ip>
   ```

2. **Install OCI CLI if needed:**
   ```bash
   sudo dnf install -y oci-cli
   ```

3. **Get Secret OCID:**
   - Go to Vault → Secrets → Your secret
   - Copy the OCID

4. **Retrieve the secret value:**
   ```bash
   oci secrets secret-bundle get \
     --secret-id <secret-ocid> \
     --query "data.\"secret-bundle-content\".content" \
     --raw-output | base64 --decode
   ```

### Expected Result

The terminal prints the secret value (e.g., `SuperSecretP@ss123`).

This confirms secure retrieval via OCI Vault.

---

## 6. Hands-On Task 4 — Use Secret in Application (Optional)

#### Purpose

Integrate secret retrieval into BharatMart application.

### Steps

1. **Create script to retrieve secret at startup:**
   ```bash
   cat > /home/opc/get-secret.sh << 'EOF'
   #!/bin/bash
   SECRET_OCID="<your-secret-ocid>"
   SECRET_VALUE=$(oci secrets secret-bundle get \
     --secret-id $SECRET_OCID \
     --query "data.\"secret-bundle-content\".content" \
     --raw-output | base64 --decode)
   export DATABASE_PASSWORD=$SECRET_VALUE
   EOF
   
   chmod +x /home/opc/get-secret.sh
   ```

2. **Update application startup to use secret:**
   - Source the script before starting application
   - Use `$DATABASE_PASSWORD` environment variable

---

## 7. Summary of the Hands-On

In this exercise, you:

* Created OCI Vault for secure secrets storage
* Created master encryption key
* Stored secrets securely in Vault
* Configured dynamic groups and IAM policies
* Retrieved secrets from Compute instances
* Verified secure secret access

This workflow is the foundation of secure configuration management.

---

## 8. Solutions Key (Instructor Reference)

### Expected Configuration:

* Vault: `<student-id>-vault`
* Master Key: `<student-id>-masterkey`
* Secret: `<student-id>-db-password`
* Dynamic Group: `<student-id>-dg`
* IAM Policy: Allows secret-bundle read access

### Expected Results:

* Secret stored and encrypted in Vault
* Instance can retrieve secret using instance principal
* No secrets stored in plaintext on instance
* IAM policies control access

---

## End of Hands-On Document

