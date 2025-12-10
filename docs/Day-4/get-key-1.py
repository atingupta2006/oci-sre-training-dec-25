import oci
import base64

config = oci.config.from_file()
print(config)

#config = oci.config.from_file()

# IMPORTANT → Set secrets endpoint for your region
secrets_client = oci.secrets.SecretsClient(
    config,
    service_endpoint="https://secrets.vaults.eu-frankfurt-1.oci.oraclecloud.com"
)

secret_id = "ocid1.vaultsecret.oc1.eu-frankfurt-1.amaaaaaahqssvraa3p6yz2l6nfp6d4i2jx7z5unqrlfyag3mhwuokj6ew2mq"

bundle = secrets_client.get_secret_bundle(secret_id).data
encoded = bundle.secret_bundle_content.content
decoded = base64.b64decode(encoded).decode()

print(decoded)