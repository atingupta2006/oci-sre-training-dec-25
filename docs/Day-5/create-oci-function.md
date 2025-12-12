# OCI Functions Setup & Deployment on Ubuntu (Python Fn Function)

## 1. Install Required Packages

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release unzip build-essential
```

## 2. Install Docker (get-docker)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
sudo docker run hello-world
```

## 3. Install OCI CLI

```bash
curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh | bash
exec -l $SHELL
```

## 4. Install Fn CLI

```bash
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh
export PATH=/usr/local/bin:$PATH
echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bashrc
fn version
```

## 5. Set Up Fn Context for OCI Functions

```bash
fn use context oracle
```

Edit context:

```bash
nano ~/.fn/contexts/oracle.yaml
```

Content:

```
api-url: https://functions.ap-mumbai-1.oraclecloud.com
provider: oracle
tenancy: ocid1.tenancy.oc1..aaaaaaaaqh5uemzgiwvqvikjxlxl6h5mdncebvlmbb7prcrcgglnbdsr5dqa
user: ocid1.user.oc1..aaaaaaaahzhjdcjcta3wtgapyhnq7nf6wby2t2dkbc7tlnjlorjqwqzsxk4q
fingerprint: 61:b1:d3:bd:56:07:a4:f7:b4:e0:ea:8f:d6:85:e2:ee
region: ap-mumbai-1
private-key: /home/adminadmin/.oci/oci_api_key.pem
auth-token: "<AUTH_TOKEN>"
oracle.compartment-id: ocid1.compartment.oc1..aaaaaaaavzlulwgc4twmrqqfsb5jack4i6cgq3t6yzc2rwhslppf53rrbb5q
```

Verify:

```bash
fn list apps
```

## 6. Get Object Storage Namespace

```bash
oci os ns get
```

Output used: `bm5uizuxnaa5`

## 7. Docker Login to OCIR

```bash
docker login bom.ocir.io -u bm5uizuxnaa5/atingupta2005@gmail.com -p "<PASSWORD>"
```

## 8. Set FN_REGISTRY

```bash
export FN_REGISTRY=bom.ocir.io/bm5uizuxnaa5
echo 'export FN_REGISTRY=bom.ocir.io/bm5uizuxnaa5' >> ~/.bashrc
echo $FN_REGISTRY
```

## 9. Create Function Directory

```bash
mkdir myfn && cd myfn
fn init --runtime python hello
cd hello
```

Directory:

```
~/myfn/hello
    func.py
    func.yaml
    requirements.txt
```

## 10. Update requirements.txt

```
fdk
```

## 11. Verify func.yaml

```
schema_version: 20180708
name: hello
version: 0.0.8
runtime: python
build_image: fnproject/python:3.12-dev
run_image: fnproject/python:3.12
entrypoint: /python/bin/fdk /function/func.py handler
memory: 256
```

## 12. Build Function

```bash
fn build
```

## 13. Deploy Function

```bash
fn deploy --app app-my-func
```

## 14. Invoke Function

```bash
fn invoke app-my-func hello
```

Or with JSON payload:

```bash
echo '{"name":"Atin"}' | fn invoke app-my-func hello
```

## 15. Confirm Function Exists

```bash
oci fn function list --application-id ocid1.fnapp.oc1.ap-mumbai-1.amaaaaaahqssvraawa2haq2fypbiivw3frap3zuokrtbtgywnuy3r4cgfcpq
```

## 16. View Logs (UI Only)

Logs available under:
**Observability & Management → Logging → Log Groups → Functions Log Group**

## 17. Final Working func.py

```python
import io
import json
import logging
from fdk import response

def handler(ctx, data: io.BytesIO = None):
    name = "World"
    try:
        body = json.loads(data.getvalue())
        name = body.get("name")
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    logging.getLogger().info("Inside Python Hello World function")
    return response.Response(
        ctx, response_data=json.dumps({"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )
```

## 18. Final Validation

```bash
fn invoke app-my-func hello
```
