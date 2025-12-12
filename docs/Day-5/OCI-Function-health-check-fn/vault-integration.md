# **OCI Vault Integration with Health-Check Function — Implementation Runbook**

This runbook describes how to securely integrate an OCI Function with OCI Vault using Resource Principals. It includes the complete end-to-end setup, IAM configuration, deployment steps, and validation procedure.
The document reflects the final working model that I implemented, along with stable configurations and verified patterns.

---

# **1. Objective**

Secure a serverless health-check function so it:

* Reads secrets from OCI Vault
* Uses Resource Principals (no API keys required)
* Stores only secret OCIDs in function configuration
* Maintains least-privilege IAM controls
* Supports clean troubleshooting and observability

This runbook assumes the function and vault already exist in OCI.

---

# **2. Prerequisites**

* OCI CLI + Fn CLI installed
* Fn configured with **Oracle Cloud context**
* OCIR login completed using Auth Token
* Python function directory containing:

```
func.py
func.yaml
requirements.txt
```

---

# **3. Core Variables**

```bash
APP_NAME="app-my-func"
FUNCTION_NAME="health-check"
SECRET_OCID="ocid1.vaultsecret.oc1.ap-mumbai-1.amaaaaaahqssvraausa7ls5cg2udsnkgtyq2qh6z3x3jgrlvg4umv27yfkda"
FUNCTION_COMPARTMENT_OCID="ocid1.compartment.oc1..aaaaaaaavzlulwgc4twmrqqfsb5jack4i6cgq3t6yzc2rwhslppf53rrbb5q"
DYNAMIC_GROUP_NAME="dg-fn-healthchecks"
```

---

# **4. Dynamic Group**

A dynamic group is required so the function can authenticate through Resource Principals.

**Dynamic Group Rule**

```text
Any {
  ALL {
    resource.type = 'fnfunc',
    resource.compartment.id = '<function compartment OCID>'
  }
}
```

This rule ensures the function identity is automatically matched without hardcoding OCIDs of individual functions.

---

# **5. IAM Policy Design**

OCI Vault secrets may reside in:

* A specific compartment **or**
* The **tenancy root compartment** (default location if not explicitly changed)

Policies must always be created **in the compartment where the Vault/Secret resides**.

### In this environment, the secret resides in the **Tenancy Root**, so the correct policy must be written in Root.

**Root Compartment Policy**

```
Allow dynamic-group dg-fn-healthchecks to read secret-family in tenancy
Allow dynamic-group dg-fn-healthchecks to use vaults in tenancy
```

This grants the function permission to retrieve Vault secrets using Resource Principals.

> *Note: IAM policy propagation typically takes 2–5 minutes.*

---

# **6. Function Configuration**

Store runtime parameters inside the function configuration:

```bash
fn config function $APP_NAME $FUNCTION_NAME SECRET_OCID "$SECRET_OCID"
fn config function $APP_NAME $FUNCTION_NAME REQUEST_TIMEOUT "5"
fn config function $APP_NAME $FUNCTION_NAME RETRIES "1"
fn config function $APP_NAME $FUNCTION_NAME BACKOFF_SECONDS "1.0"
fn config function $APP_NAME $FUNCTION_NAME LATENCY_THRESHOLD_MS "1000"
fn config function $APP_NAME $FUNCTION_NAME ORDERS_FAILED_THRESHOLD "0"
```

Verify:

```bash
fn inspect function $APP_NAME $FUNCTION_NAME
```

---

# **7. Requirements File (Final Working Version)**

```
fdk
requests
oci
urllib3<2
```

This ensures the OCI Python SDK is available inside the function container.

---

# **8. Final Function Code**

```python
import io
import json
import logging
import base64
import os
from datetime import datetime
import requests
from fdk import response
import oci

def handler(ctx, data: io.BytesIO = None):
    # -------------------------------------------------------------------
    # Retrieve secret from OCI Vault using Resource Principals
    # -------------------------------------------------------------------
    secret_value = None
    secret_ocid = os.getenv("SECRET_OCID")

    try:
        signer = oci.auth.signers.get_resource_principals_signer()
        secrets_client = oci.secrets.SecretsClient(config={}, signer=signer)

        resp = secrets_client.get_secret_bundle(secret_id=secret_ocid)
        raw = resp.data.secret_bundle_content.content
        secret_value = base64.b64decode(raw).decode("utf-8")

        logging.getLogger().info("Vault secret retrieved successfully.")
    except Exception as e:
        logging.getLogger().error(f"Vault retrieval error: {e}")
        secret_value = f"ERROR: {str(e)}"

    # -------------------------------------------------------------------
    # Perform target health check
    # -------------------------------------------------------------------
    url = "http://161.118.191.254/api/health"
    try:
        r = requests.get(url, timeout=5)
        health_status = {
            "target": url,
            "status": "healthy" if r.status_code == 200 else "unhealthy",
            "status_code": r.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        health_status = {
            "target": url,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

    # -------------------------------------------------------------------
    # Final response (for testing; secret should be removed in prod)
    # -------------------------------------------------------------------
    response_body = {
        "health_check": health_status,
        "secret_value": secret_value
    }

    logging.getLogger().info(json.dumps(response_body))

    return response.Response(
        ctx,
        response_data=json.dumps(response_body),
        headers={"Content-Type": "application/json"}
    )
```

---

# **9. Deployment**

From the function directory:

```bash
fn build
fn deploy --app $APP_NAME
```

(Ensure OCIR login is already done.)

---

# **10. Validation**

Invoke:

```bash
fn invoke $APP_NAME $FUNCTION_NAME
```

Successful output:

```json
{
  "health_check": { ... },
  "secret_value": "your-secret-value"
}
```

This confirms:

* Resource Principals are working
* Dynamic group rule is correct
* Root-level policy is correct
* Secret exists and is readable
* Python SDK is installed

---

# **11. Key Implementation Notes**

* Functions cannot read Vault secrets unless IAM policy exists **in the same compartment where the secret is stored**
* Secrets placed in the **tenancy root** require **root-level policies**
* Missing OCI SDK in `requirements.txt` will cause immediate runtime failure
* OCIR authorization requires Docker login using Auth Token
* IAM policy changes take a few minutes to propagate
* For production, never return the secret value in the response

---

# **12. Recommended Best Practices**

* Store Vault Keys, Vaults, and Secrets in a dedicated security compartment
* Keep function code logging minimal and avoid exposing sensitive data
* Apply least-privilege policies
* Monitor function logs through OCI Logging service
* Redact secret output after initial testing
