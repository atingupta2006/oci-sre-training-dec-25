# **OCI – Working with Vault Secrets**

## **1. Retrieve Secret Using OCI CLI**

Get the latest version of the secret:

```bash
oci secrets secret-bundle get \
  --secret-id "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaahqssvraa3p6yz2l6nfp6d4i2jx7z5unqrlfyag3mhwuokj6ew2mq" \
  --stage CURRENT \
  --query "data.\"secret-bundle-content\".content" \
  --raw-output
```

Id the the output is base64-encoded. To decode:

```bash
echo "<BASE64_VALUE>" | base64 --decode
```

---

## **2. Retrieve Secret Using Python**
 - Note: Tested and working on Ubuntu non OCI VM
```
ssh opc@130.61.210.235
source ~/venv/bin/activate
nano get-key-1.py
python get-key-1.py
exit
```

```python
import oci
import base64

# Load OCI config (assumes ~/.oci/config is already set)
config = oci.config.from_file()

# Secrets endpoint for your region
endpoint = "https://secrets.vaults.eu-frankfurt-1.oci.oraclecloud.com"

client = oci.secrets.SecretsClient(config, service_endpoint=endpoint)

secret_id = "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaahqssvraa3p6yz2l6nfp6d4i2jx7z5unqrlfyag3mhwuokj6ew2mq"

bundle = client.get_secret_bundle(secret_id).data
encoded = bundle.secret_bundle_content.content
decoded = base64.b64decode(encoded).decode()

print(decoded)
```

---

## **3. Retrieve Using Instance Principals (Optional – OCI Compute)**
 - Note: Tested and working on OCI Frontend VM
```
ssh opc@130.61.210.235
source ~/venv/bin/activate
nano get-key-2.py
python get-key-2.py
exit
```


```python
import oci
import base64

signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

client = oci.secrets.SecretsClient(
    config={},
    signer=signer,
    service_endpoint="https://secrets.vaults.eu-frankfurt-1.oci.oraclecloud.com"
)

secret_id = "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaahqssvraa3p6yz2l6nfp6d4i2jx7z5unqrlfyag3mhwuokj6ew2mq"
bundle = client.get_secret_bundle(secret_id).data

decoded = base64.b64decode(bundle.secret_bundle_content.content).decode()
print(decoded)
```

```
oci secrets secret-bundle get   --secret-id "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaahqssvraa3p6yz2l6nfp6d4i2jx7z5unqrlfyag3mhwuokj6ew2mq"   --stage CURRENT   --query "data.\"secret-bundle-content\".content"   --raw-output --auth instance_principal
DEBUG:oci_cli.cli_util:Check if Propagation Enabled: None
DEBUG:oci_cli.cli_util:Is Propagation Enabled: None
c2Ztc2ZtQDE0NDU=
```