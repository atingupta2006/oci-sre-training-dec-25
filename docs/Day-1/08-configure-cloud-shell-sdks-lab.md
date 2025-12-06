# Day 1: Configure Cloud Shell and SDKs for Automation (Hands-on Lab)

### Audience Context: IT Engineers and Developers

---

## 0. Deployment Assumptions

For this hands-on lab, you will configure OCI Cloud Shell and SDKs on your own OCI account.

**Prerequisites:**

* OCI tenancy with user account
* Browser access to OCI Console

---

## 1. Purpose

OCI Cloud Shell provides a browser-based terminal environment with pre-configured OCI CLI and SDKs. This lab shows you how to access and configure Cloud Shell for SRE automation tasks.

---

## 2. Steps

#### Step 1: Access OCI Cloud Shell

1. Log in to **OCI Console**: [https://cloud.oracle.com](https://cloud.oracle.com)
2. Click the **Cloud Shell icon** (terminal icon) in the top navigation bar
3. Wait for Cloud Shell to initialize (first-time setup may take 30-60 seconds)

#### Step 2: Verify OCI CLI Installation

1. Check OCI CLI version:
   ```bash
   oci --version
   ```
   Expected output: `oci version 3.x.x` or similar

2. Verify OCI CLI is configured:
   ```bash
   oci iam region list
   ```
   Expected: List of available OCI regions

#### Step 3: Configure OCI CLI (if needed)

If OCI CLI is not configured, run:

```bash
oci setup config
```

Follow the prompts:

* **Enter location for config file:** Press Enter (default: `~/.oci/config`)
* **Enter a user OCID:** Your user OCID (found in User Settings → User Information)
* **Enter a tenancy OCID:** Your tenancy OCID (found in Administration → Tenancy Details)
* **Enter a region:** Select a region (e.g., `us-ashburn-1`)
* **Generate API signing key:** Press Enter to generate automatically
* **Enter passphrase:** Set a passphrase or press Enter for no passphrase

#### Step 4: Set Up Python Virtual Environment

1. **Check Python version:**
   ```bash
   python3 --version
   ```
   Expected: Python 3.8 or later

2. **Create a virtual environment:**
   ```bash
   python3 -m venv ~/oci-env
   ```

3. **Activate the virtual environment:**
   ```bash
   source ~/oci-env/bin/activate
   ```
   Your prompt should now show `(oci-env)` indicating the virtual environment is active.

4. **Install OCI Python SDK in the virtual environment:**
   ```bash
   pip install oci
   ```

#### Step 5: Verify Python SDK Availability

1. **Verify OCI Python SDK is installed:**
   ```bash
   python3 -c "import oci; print(f'OCI SDK version: {oci.__version__}')"
   ```
   Expected: OCI SDK version number (e.g., `OCI SDK version: 2.x.x`)

2. **Note:** Always activate the virtual environment before using Python SDK:
   ```bash
   source ~/oci-env/bin/activate
   ```

#### Step 6: Test OCI CLI Access

1. List compartments:
   ```bash
   oci iam compartment list --compartment-id <tenancy-ocid> --all
   ```
   Replace `<tenancy-ocid>` with your tenancy OCID

2. List compute instances (if any exist):
   ```bash
   oci compute instance list --compartment-id <compartment-ocid> --all
   ```
   Replace `<compartment-ocid>` with a compartment OCID from previous step

#### Step 7: Test Python SDK Access

**Important:** Ensure the virtual environment is activated before running Python scripts.

1. **Activate virtual environment (if not already active):**
   ```bash
   source ~/oci-env/bin/activate
   ```

2. **Create a test script:**
   ```bash
   cat > ~/test_oci_sdk.py << 'EOF'
   #!/usr/bin/env python3
   import oci

   # Load default config
   config = oci.config.from_file()

   # Create Identity client
   identity = oci.identity.IdentityClient(config)

   # List compartments
   response = identity.list_compartments(
       compartment_id=config['tenancy'],
       compartment_id_in_subtree=True
   )

   print("Compartments:")
   for compartment in response.data:
       print(f"  - {compartment.name} ({compartment.id})")
   EOF
   ```

3. **Make script executable:**
   ```bash
   chmod +x ~/test_oci_sdk.py
   ```

4. **Run the test script:**
   ```bash
   python3 ~/test_oci_sdk.py
   ```

Expected: List of compartments in your tenancy

#### Step 8: Create Useful Aliases (Optional)

Add aliases to your `~/.bashrc` for common OCI operations:

```bash
cat >> ~/.bashrc << 'EOF'

# OCI CLI aliases
alias oci-compartments='oci iam compartment list --compartment-id-in-subtree true --all'
alias oci-instances='oci compute instance list --compartment-id-in-subtree true --all'
alias oci-regions='oci iam region list'
EOF

source ~/.bashrc
```

---

## 3. What You Should See

* Cloud Shell terminal accessible from OCI Console
* OCI CLI working and configured
* Python virtual environment created and activated
* OCI Python SDK installed in virtual environment
* Successful API calls to list compartments and instances

---

## 4. Troubleshooting

* **Cloud Shell won't start:** Check browser console for errors, try refreshing
* **OCI CLI not configured:** Run `oci setup config` again
* **Permission denied:** Verify your user has appropriate IAM policies
* **Python SDK not found:** Ensure virtual environment is activated, then install with `pip install oci`
* **ModuleNotFoundError:** Make sure you've activated the virtual environment with `source ~/oci-env/bin/activate`

---

## 5. Key Takeaways

* Cloud Shell provides immediate access to OCI CLI and SDKs without local installation
* Virtual environments isolate Python packages and prevent conflicts
* OCI CLI enables automation of infrastructure management tasks
* Python SDK provides programmatic access to OCI services for custom automation
* Always activate virtual environment before using Python SDK
* These tools will be used throughout the training for SRE automation tasks

