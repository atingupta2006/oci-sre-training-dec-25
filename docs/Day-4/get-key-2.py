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