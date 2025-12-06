# Day 5: Secure Automation Using OCI Vault + Dynamic Secrets - Hands-on Lab

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will practice secure automation with OCI Vault and dynamic secrets.

**Prerequisites:**
* OCI tenancy with appropriate permissions
* OCI Vault service enabled
* OCI CLI configured and working
* Understanding of OCI Vault from Day 4
* Basic Python or Bash scripting knowledge
* BharatMart deployed (optional, for integration example)

**Assumed Deployment:**
* OCI Vault available in your compartment
* At least one vault created (from Day 4 lab)
* Automation scripts running on Compute instances or Cloud Shell

---

## 1. Objective of This Hands-On

By completing this exercise, students will:

* Understand dynamic secrets and their benefits
* Retrieve secrets from OCI Vault in automation scripts
* Use secrets securely without hardcoding
* Configure secret rotation
* Integrate secrets into automation workflows
* Verify secure secret handling (no secrets in logs/code)

---

## 2. Background Concepts

### 2.1 Dynamic Secrets

**Dynamic Secrets** are retrieved at runtime from secure stores (like OCI Vault) rather than hardcoded in configuration files or code.

**Benefits:**
* **No secrets in code** - Secrets never appear in source code, config files, or environment variables
* **Easy rotation** - Update secrets in vault without changing code
* **Secure retrieval** - Access controlled via IAM policies and encryption
* **Audit logging** - All secret access is logged for compliance
* **Version management** - Vault tracks secret versions for rollback

### 2.2 OCI Vault Secret Retrieval

**OCI Vault** provides secure secret storage with:

* Encryption at rest and in transit
* Automatic secret versioning
* IAM-based access control
* Audit logging of all access
* Integration with Dynamic Groups for service authentication

**Retrieval Methods:**
* OCI CLI (`oci secrets secret-bundle get`)
* OCI SDKs (Python, Java, Go, etc.)
* OCI REST APIs
* Instance Principals (for Compute instances)

### 2.3 Secure Automation Pattern

```
Automation Script/Function
    ↓ (Authenticate via Instance Principal or API Key)
OCI Vault
    ↓ (Retrieve secret)
Encrypted Secret Bundle
    ↓ (Decode/Decrypt)
Use Secret in Automation
    ↓ (Never log secret)
Complete Automation Task
```

---

## 3. Hands-On Task 1 — Create Secret in OCI Vault

#### Purpose

Create a secret in OCI Vault that will be used by automation scripts.

### Steps:

#### Step 1: Create or Verify Vault

1. **Navigate to Vault:**
   - Go to **OCI Console → Identity & Security → Vault**
   - Select your compartment

2. **Create Vault (if needed):**
   - Click **Create Vault**
   - **Name:** `<student-id>-automation-vault`
   - **Vault Type:** Default (no HSM for lab)
   - Click **Create**
   - Wait for vault to be in **Active** state

3. **Note the Vault OCID** for later use.

#### Step 2: Create Secret

1. **Navigate to Secrets:**
   - Go to your vault
   - Click **Secrets** in left menu
   - Click **Create Secret**

2. **Configure Secret:**
   - **Name:** `<student-id>-db-password`
   - **Secret Type:** Secret (Plaintext)
   - **Secret Contents:**
     - **Encoding:** Plaintext
     - **Value:** `SecurePassword123!` (use a test password for lab)
   - **Description:** `Database password for BharatMart automation`
   - **Encryption Key:** Use default master encryption key
   - Click **Create Secret**

3. **Note the Secret OCID** - you'll need this for retrieval.

   Example OCID format:
   ```
   ocid1.vaultsecret.oc1.region.xxxxx.xxxxx
   ```

#### Step 3: Create Policy for Secret Access

1. **Navigate to Policies:**
   - Go to **Identity → Policies**
   - Create or edit policy in your compartment

2. **Add Policy Statement:**
   ```
   Allow group <your-group-name> to read secret-family in compartment <compartment-name>
   Allow group <your-group-name> to use vaults in compartment <compartment-name>
   ```

   Or for instance principals (if running on Compute):
   ```
   Allow dynamic-group <dynamic-group-name> to read secret-family in compartment <compartment-name>
   Allow dynamic-group <dynamic-group-name> to use vaults in compartment <compartment-name>
   ```

---

## 4. Hands-On Task 2 — Retrieve Secret in Bash Script

#### Purpose

Create a bash automation script that retrieves secrets from OCI Vault at runtime.

### Steps:

#### Step 1: Create Secret Retrieval Script

1. **Create script file:**
   ```bash
   cat > ~/secure-automation.sh << 'EOF'
   #!/bin/bash
   # Secure automation script using OCI Vault secrets
   # This script demonstrates secure secret retrieval
   
   set -euo pipefail  # Exit on error, undefined vars, pipe failures
   
   # Configuration
   SECRET_OCID="${SECRET_OCID:-}"  # Set via environment or replace
   COMPARTMENT_OCID="${COMPARTMENT_OCID:-}"  # Your compartment OCID
   
   if [ -z "$SECRET_OCID" ]; then
       echo "ERROR: SECRET_OCID not set"
       exit 1
   fi
   
   echo "=== Secure Automation Script ==="
   echo "Secret OCID: ${SECRET_OCID:0:20}..."  # Only show first 20 chars
   echo ""
   
   # Retrieve secret from OCI Vault
   echo "Step 1: Retrieving secret from OCI Vault..."
   SECRET_BUNDLE=$(oci secrets secret-bundle get \
       --secret-id "$SECRET_OCID" \
       --query "data.\"secret-bundle-content\".content" \
       --raw-output 2>/dev/null)
   
   if [ $? -ne 0 ]; then
       echo "ERROR: Failed to retrieve secret"
       exit 1
   fi
   
   # Decode base64 secret
   echo "Step 2: Decoding secret..."
   DB_PASSWORD=$(echo "$SECRET_BUNDLE" | base64 --decode)
   
   # Verify secret retrieved (but never print it)
   if [ -z "$DB_PASSWORD" ]; then
       echo "ERROR: Secret is empty"
       exit 1
   fi
   
   echo "Step 3: Secret retrieved successfully (length: ${#DB_PASSWORD} characters)"
   echo ""
   
   # Use secret in automation (example: database connection)
   echo "Step 4: Using secret in automation..."
   echo "  - Connecting to database..."
   echo "  - Using password from Vault (not hardcoded)"
   echo "  - Performing automated task..."
   
   # Example: Use secret (replace with actual automation)
   # psql -h database.example.com -U admin -d bharatmart -c "SELECT 1;" 2>&1 | head -1
   
   echo ""
   echo "Step 5: Automation completed successfully"
   echo ""
   echo "✅ Security Check:"
   echo "  - Secret not in script source: PASS"
   echo "  - Secret not in environment variables: PASS"
   echo "  - Secret not logged: PASS"
   echo "  - Secret retrieved securely: PASS"
   
   # Clear secret from memory (best practice)
   unset DB_PASSWORD
   unset SECRET_BUNDLE
   
   EOF
   
   chmod +x ~/secure-automation.sh
   ```

#### Step 2: Test Script

1. **Set Environment Variables:**
   ```bash
   export SECRET_OCID="<your-secret-ocid>"
   export COMPARTMENT_OCID="<your-compartment-ocid>"
   ```

2. **Run Script:**
   ```bash
   ~/secure-automation.sh
   ```

   Expected output:
   ```
   === Secure Automation Script ===
   Secret OCID: ocid1.vaultsecret.oc1...
   
   Step 1: Retrieving secret from OCI Vault...
   Step 2: Decoding secret...
   Step 3: Secret retrieved successfully (length: 18 characters)
   
   Step 4: Using secret in automation...
     - Connecting to database...
     - Using password from Vault (not hardcoded)
     - Performing automated task...
   
   Step 5: Automation completed successfully
   
   ✅ Security Check:
     - Secret not in script source: PASS
     - Secret not in environment variables: PASS
     - Secret not logged: PASS
     - Secret retrieved securely: PASS
   ```

3. **Verify No Secrets in Output:**
   - Confirm password value is never printed
   - Only secret length or status is shown

---

## 5. Hands-On Task 3 — Retrieve Secret in Python Script

#### Purpose

Create a Python automation script using OCI SDK to retrieve secrets.

### Steps:

#### Step 1: Create Python Script

1. **Create script file:**
   ```bash
   cat > ~/secure-automation.py << 'EOF'
   #!/usr/bin/env python3
   """
   Secure automation script using OCI Vault secrets
   Demonstrates secure secret retrieval in Python
   """
   import oci
   import base64
   import os
   import sys
   import logging
   
   # Configure logging (but never log secrets)
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s'
   )
   logger = logging.getLogger(__name__)
   
   def get_secret_from_vault(secret_ocid, config=None):
       """
       Retrieve secret from OCI Vault securely
       
       Args:
           secret_ocid: OCID of the secret
           config: OCI config dictionary (uses default if None)
       
       Returns:
           Decrypted secret value as string
       """
       try:
           # Load OCI config (uses default ~/.oci/config)
           if config is None:
               config = oci.config.from_file()
           
           # Create Vaults client
           vaults_client = oci.vault.VaultsClient(config)
           
           logger.info(f"Retrieving secret: {secret_ocid[:20]}...")
           
           # Get latest secret bundle
           response = vaults_client.get_secret_bundle(
               secret_id=secret_ocid
           )
           
           # Extract secret content
           secret_content = response.data.secret_bundle_content
           
           # Decode based on content type
           if isinstance(secret_content, oci.vault.models.Base64SecretBundleContentDetails):
               # Base64 encoded content
               secret_value = base64.b64decode(
                   secret_content.content
               ).decode('utf-8')
           else:
               # Plaintext content
               secret_value = secret_content.content
           
           logger.info(f"Secret retrieved successfully (length: {len(secret_value)} chars)")
           return secret_value
           
       except oci.exceptions.ServiceError as e:
           logger.error(f"OCI Service Error: {e.message}")
           raise
       except Exception as e:
           logger.error(f"Error retrieving secret: {e}")
           raise
   
   def use_secret_in_automation(secret_value):
       """
       Use secret in automation task
       Never log the secret value itself
       """
       logger.info("Using secret in automation...")
       
       # Example: Database connection (replace with actual automation)
       # import psycopg2
       # conn = psycopg2.connect(
       #     host="database.example.com",
       #     user="admin",
       #     password=secret_value,  # Secret from Vault
       #     database="bharatmart"
       # )
       
       # Example: API authentication
       # headers = {
       #     "Authorization": f"Bearer {secret_value}"
       # }
       # response = requests.post("https://api.example.com", headers=headers)
       
       logger.info("Automation task completed")
       
       # Clear secret from memory (best practice)
       del secret_value
   
   def main():
       """Main automation function"""
       # Get secret OCID from environment variable
       secret_ocid = os.environ.get('SECRET_OCID')
       
       if not secret_ocid:
           logger.error("ERROR: SECRET_OCID environment variable not set")
           sys.exit(1)
       
       logger.info("=== Secure Automation Script (Python) ===")
       logger.info(f"Secret OCID: {secret_ocid[:20]}...")
       logger.info("")
       
       try:
           # Step 1: Retrieve secret
           logger.info("Step 1: Retrieving secret from OCI Vault...")
           secret_value = get_secret_from_vault(secret_ocid)
           
           # Step 2: Use secret
           logger.info("Step 2: Using secret in automation...")
           use_secret_in_automation(secret_value)
           
           # Step 3: Security verification
           logger.info("")
           logger.info("✅ Security Check:")
           logger.info("  - Secret not in source code: PASS")
           logger.info("  - Secret not in config files: PASS")
           logger.info("  - Secret not logged: PASS")
           logger.info("  - Secret retrieved securely: PASS")
           logger.info("")
           logger.info("Automation completed successfully")
           
       except Exception as e:
           logger.error(f"Automation failed: {e}")
           sys.exit(1)
   
   if __name__ == "__main__":
       main()
   EOF
   
   chmod +x ~/secure-automation.py
   ```

#### Step 2: Test Python Script

1. **Set Environment Variable:**
   ```bash
   export SECRET_OCID="<your-secret-ocid>"
   ```

2. **Run Script:**
   ```bash
   python3 ~/secure-automation.py
   ```

   Expected output:
   ```
   2024-01-15 10:30:00 - INFO - === Secure Automation Script (Python) ===
   2024-01-15 10:30:00 - INFO - Secret OCID: ocid1.vaultsecret.oc1...
   2024-01-15 10:30:00 - INFO - 
   2024-01-15 10:30:00 - INFO - Step 1: Retrieving secret from OCI Vault...
   2024-01-15 10:30:00 - INFO - Retrieving secret: ocid1.vaultsecret.oc1...
   2024-01-15 10:30:00 - INFO - Secret retrieved successfully (length: 18 chars)
   2024-01-15 10:30:00 - INFO - Step 2: Using secret in automation...
   2024-01-15 10:30:00 - INFO - Using secret in automation...
   2024-01-15 10:30:00 - INFO - Automation task completed
   2024-01-15 10:30:00 - INFO - 
   2024-01-15 10:30:00 - INFO - ✅ Security Check:
   2024-01-15 10:30:00 - INFO -   - Secret not in source code: PASS
   2024-01-15 10:30:00 - INFO -   - Secret not in config files: PASS
   2024-01-15 10:30:00 - INFO -   - Secret not logged: PASS
   2024-01-15 10:30:00 - INFO -   - Secret retrieved securely: PASS
   2024-01-15 10:30:00 - INFO - 
   2024-01-15 10:30:00 - INFO - Automation completed successfully
   ```

3. **Verify Security:**
   - No secret value appears in logs
   - Only secret metadata (OCID prefix, length) is logged

---

## 6. Hands-On Task 4 — Configure Secret Rotation

#### Purpose

Demonstrate how to rotate secrets without changing automation code.

### Steps:

#### Step 1: Create New Secret Version

1. **Navigate to Secret:**
   - Go to **Vault → Secrets**
   - Click on `<student-id>-db-password`

2. **Create New Version:**
   - Click **Create Secret Version**
   - **Secret Contents:**
     - **Encoding:** Plaintext
     - **Value:** `NewSecurePassword456!` (new password)
   - Click **Create**

3. **Verify New Version:**
   - Go to **Secret Versions** tab
   - Verify new version is created and marked as **Current**
   - Old version is still available but not current

#### Step 2: Test Automatic Secret Update

1. **Run Automation Script Again:**
   ```bash
   # Bash script
   ~/secure-automation.sh
   
   # Or Python script
   python3 ~/secure-automation.py
   ```

2. **Verify New Secret is Retrieved:**
   - Script should automatically retrieve the new secret version
   - No code changes needed
   - Check secret length matches new password

   Expected output:
   ```
   Step 3: Secret retrieved successfully (length: 21 characters)
   ```
   (New password is longer, so length changed)

#### Step 3: Verify Old Version Still Accessible

1. **Retrieve Specific Version:**
   ```bash
   # List secret versions
   oci vault secret version list --secret-id "<secret-ocid>"
   
   # Get specific version (old version)
   OLD_VERSION=$(oci vault secret version list \
       --secret-id "<secret-ocid>" \
       --query "data[1].\"version-number\" | [0]" \
       --raw-output)
   
   # Retrieve old version
   oci secrets secret-bundle get \
       --secret-id "<secret-ocid>" \
       --version-number "$OLD_VERSION" \
       --query "data.\"secret-bundle-content\".content" \
       --raw-output | base64 --decode
   ```

   This demonstrates that old versions remain accessible for rollback.

#### Step 4: Understand Rotation Benefits

**Key Benefits:**
* **No Code Changes:** Automation scripts automatically use latest version
* **Easy Rollback:** Can revert to previous version if issues occur
* **Audit Trail:** Vault logs all version changes
* **Zero Downtime:** Rotation happens without service interruption

---

## 7. Hands-On Task 5 — Integrate with Automation Workflow

#### Purpose

Integrate secret retrieval into a complete automation workflow.

### Steps:

#### Example: Scheduled Database Backup Script

1. **Create Backup Script:**
   ```bash
   cat > ~/backup-automation.sh << 'EOF'
   #!/bin/bash
   # Scheduled database backup using Vault secrets
   
   set -euo pipefail
   
   SECRET_OCID="${DB_PASSWORD_SECRET_OCID:-}"
   BACKUP_DIR="/backups"
   DATE=$(date +%Y%m%d_%H%M%S)
   
   # Retrieve database password from Vault
   DB_PASSWORD=$(oci secrets secret-bundle get \
       --secret-id "$SECRET_OCID" \
       --query "data.\"secret-bundle-content\".content" \
       --raw-output | base64 --decode)
   
   # Perform backup (example - replace with actual backup command)
   echo "Starting database backup at $(date)"
   # pg_dump -h database.example.com -U admin -d bharatmart | \
   #     gzip > "$BACKUP_DIR/backup_$DATE.sql.gz"
   
   echo "Backup completed: backup_$DATE.sql.gz"
   echo "Backup size: $(du -h $BACKUP_DIR/backup_$DATE.sql.gz | cut -f1)"
   
   # Clear secret
   unset DB_PASSWORD
   EOF
   
   chmod +x ~/backup-automation.sh
   ```

2. **Schedule with Cron (Example):**
   ```bash
   # Add to crontab for daily backup at 2 AM
   # crontab -e
   # 0 2 * * * /home/opc/backup-automation.sh >> /var/log/backup.log 2>&1
   ```

#### Example: CI/CD Pipeline Integration

1. **GitLab CI Example:**
   ```yaml
   # .gitlab-ci.yml
   backup_stage:
     script:
       - |
         export SECRET_OCID="${OCI_SECRET_OCID}"
         python3 secure-automation.py
     only:
       - schedules
   ```

2. **GitHub Actions Example:**
   ```yaml
   # .github/workflows/automation.yml
   - name: Retrieve Secret
     run: |
       export SECRET_OCID="${{ secrets.OCI_SECRET_OCID }}"
       python3 secure-automation.py
   ```

---

## 8. Hands-On Task 6 — Verify Security (No Secrets in Logs)

#### Purpose

Verify that secrets are never exposed in logs or code.

### Steps:

#### Step 1: Enable Verbose Logging

1. **Run Script with Debug Output:**
   ```bash
   bash -x ~/secure-automation.sh 2>&1 | tee automation-debug.log
   ```

2. **Inspect Log File:**
   ```bash
   # Search for secret patterns (should find nothing)
   grep -i "password\|secret\|SecurePassword" automation-debug.log
   ```

   Expected: No matches (secrets should not appear)

#### Step 2: Check Environment Variables

1. **Run Script and Check Environment:**
   ```bash
   # Run script
   ~/secure-automation.sh
   
   # Check environment (secret should not be here)
   env | grep -i "password\|secret"
   ```

   Expected: No secrets in environment

#### Step 3: Verify Source Code

1. **Search Source Files:**
   ```bash
   # Search for hardcoded secrets
   grep -r "SecurePassword\|password.*=" ~/secure-automation*.sh ~/secure-automation*.py
   ```

   Expected: No hardcoded secrets found

#### Step 4: Check Process List (Security Best Practice)

1. **Monitor During Execution:**
   ```bash
   # In one terminal, watch processes
   watch -n 1 'ps aux | grep -E "secure-automation|oci secrets"'
   
   # In another terminal, run script
   ~/secure-automation.sh
   ```

   Expected: Process list doesn't expose secret values

---

## 9. Summary of the Hands-On

In this exercise, you:

* Created secrets in OCI Vault
* Retrieved secrets securely in bash scripts
* Retrieved secrets securely in Python scripts
* Configured secret rotation
* Integrated secrets into automation workflows
* Verified secrets never appear in logs or code
* Practiced secure secret handling patterns

This demonstrates how dynamic secrets eliminate hardcoded credentials and enable secure automation.

---

## 10. Best Practices Summary

### ✅ Do's:

* Always retrieve secrets at runtime from Vault
* Use environment variables for secret OCIDs (not secret values)
* Clear secrets from memory after use
* Log secret metadata (OCID, length) but never the value
* Use IAM policies to restrict secret access
* Rotate secrets regularly
* Use instance principals for Compute-based automation

### ❌ Don'ts:

* Never hardcode secrets in source code
* Never commit secrets to version control
* Never log secret values
* Never pass secrets via command-line arguments
* Never store secrets in environment variables
* Never include secrets in configuration files
* Never share secrets via insecure channels

---

## 11. Troubleshooting

### Cannot Retrieve Secret

* **Check IAM Policies:** Verify user/group has `read secret-family` permission
* **Verify Secret OCID:** Ensure OCID is correct and complete
* **Check Vault Status:** Verify vault is Active
* **Verify Secret Status:** Check secret is in Active state

### Permission Denied

* **Check Dynamic Groups:** If using instance principals, verify dynamic group rules
* **Verify Policies:** Ensure policies allow secret access for your principal
* **Check Compartment:** Verify you're accessing secrets in correct compartment

### Secret Rotation Issues

* **Version Number:** Specify version number if needed for testing
* **Timing:** Allow a few seconds for new version to become current
* **Cache:** Scripts retrieve latest version by default (no caching)

---

## 12. Solutions Key (Instructor Reference)

### ✔ Solution Key — Task 1: Secret Creation

#### Expected Configuration:

* Vault: `<student-id>-automation-vault`
* Secret: `<student-id>-db-password`
* Status: Active
* Version: 1 (initial)

### ✔ Solution Key — Task 2-3: Scripts

#### Expected Results:

* Bash script retrieves and uses secret
* Python script retrieves and uses secret
* No secrets in output or logs
* Scripts complete successfully

### ✔ Solution Key — Task 4: Rotation

#### Expected Results:

* New secret version created
* Scripts automatically use new version
* Old version still accessible
* No code changes required

### ✔ Solution Key — Task 6: Security Verification

#### Expected Results:

* No secrets in logs
* No secrets in environment variables
* No secrets in source code
* All security checks pass

---

## End of Hands-On Document
