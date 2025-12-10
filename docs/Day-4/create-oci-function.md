# OCI Functions on Ubuntu
## 1. Prerequisites

Ensure the following are installed:

### 1.1 OCI CLI (configured with working API key)

```
oci iam region list
```

If this prints regions, authentication works.

### 1.2 Fn CLI

```
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh
fn version
```

### 1.3 Docker

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

Logout/login and test:

```
docker run hello-world
```

---

## 2. Get Required OCI Details

### 2.1 Get your Object Storage namespace

```
oci os ns get --query data --raw-output
```

Save it as a variable:

```
NAMESPACE=$(oci os ns get --query data --raw-output)
```

### 2.2 Get your region (read directly from config)

```
REGION=$(grep '^region=' ~/.oci/config | cut -d'=' -f2)
echo "$REGION"
```

REGION=$(oci configure get region)

```

### 2.3 Get tenancy OCID
```

TENANCY_OCID=$(grep '^tenancy=' ~/.oci/config | cut -d'=' -f2)
echo "$TENANCY_OCID"

```

TENANCY_OCID=$(oci configure get tenancy)
```

---

## 3. Authenticate Docker to OCIR

Create an auth token in OCI Console → User → Auth Tokens.

Then login (Frankfurt example):

```
echo -n "<AUTH_TOKEN>" | docker login -u "$NAMESPACE/<your-username>" --password-stdin fra.ocir.io
```

Replace region endpoint if different.

---

## 4. Create an OCI Function Application

Requires a **private subnet OCID** from your VCN.

```
APP_NAME="my-fn-app"
SUBNET_OCID="<YOUR_SUBNET_OCID>"

oci fn application create \
  --compartment-id "$TENANCY_OCID" \
  --display-name "$APP_NAME" \
  --subnet-id "$SUBNET_OCID"
```

Get the app OCID:

```
APP_OCID=$(oci fn application list \
  --compartment-id "$TENANCY_OCID" \
  --query "data[?\"display-name\"=='$APP_NAME'].id | [0]" \
  --raw-output)
```

---

## 5. Configure Fn Context for OCI

```
fn create context oci --provider oracle
fn use context oci
fn update context oracle.compartment-id "$TENANCY_OCID"
fn update context oracle.profile DEFAULT
fn update context oracle.region "$REGION"
fn update context api-url "https://functions.$REGION.oci.oraclecloud.com"
```

Verify:

```
fn context view
```

---

## 6. Create Hello World Function (Python Example)

```
fn init --runtime python hello-fn
cd hello-fn
```

Edit `func.py` if needed (default is fine):

```
def handler(ctx, data=None):
    return {"message": "Hello from OCI Function!"}
```

---

## 7. Deploy the Function

```
fn -v deploy --app $APP_NAME
```

This will:

* build Docker image
* push to OCIR
* register the function

---

## 8. Invoke the Function

### 8.1 Get the function OCID

```
FUNCTION_OCID=$(oci fn function list \
  --application-id "$APP_OCID" \
  --query "data[0].id" \
  --raw-output)
```

### 8.2 Invoke

```
oci fn function invoke \
  --function-id "$FUNCTION_OCID" \
  --file /dev/stdout
```

Expected output:

```
{"message": "Hello from OCI Function!"}
```

---

## 9. Clean Up (Optional)

Delete function:

```
oci fn function delete --function-id "$FUNCTION_OCID" --force
```

Delete application:

```
oci fn application delete --application-id "$APP_OCID" --force
```
