# 🚀 **BharatMart Application Deployment on OCI VMs**

Your Terraform deployment has provisioned:

### ✅ **Frontend VM (Public Subnet, Public IP)**

* Public IP from Terraform output: **141.148.217.172**
* LB serves frontend via: **[http://161.118.164.93](http://161.118.164.93)**

### ✅ **Backend VM (Private Subnet, Private IP Only)**

* Private IP from Terraform output: **10.0.2.14**
* Backend accessed via LB on: **[http://161.118.164.93:3000](http://161.118.164.93:3000)**

### ✅ **Load Balancer**

Handles:

* **Port 80 → Frontend VM**
* **Port 3000 → Backend API**

---

# ✅ **1. Connect to Your VMs**

---

## **1.1 SSH into Frontend VM**

```
scp -i ~/.ssh/id_rsa /home/adminuser/.ssh/id_rsa opc@141.148.217.172:~/.ssh
scp -i ~/.ssh/id_rsa /home/adminuser/.ssh/id_rsa.pub opc@141.148.217.172:~/.ssh
```


```bash
ssh -i ~/.ssh/id_rsa opc@141.148.217.172
```

(Use **frontend_public_ips** output)

---

## **1.2 SSH into Backend VM (via Frontend VM)**

Backend has **no public IP**, so connect via frontend VM.

From FRONTEND VM:

```bash
ssh -i ~/id_rsa opc@10.0.2.14
```

(Use **backend_private_ips** output)

---

# 📦 **2. Install Dependencies (Both VMs)**

```bash
sudo yum update -y
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs git
```

Verify:

```bash
node --version
npm --version
```

---

# 📁 **3. Download BharatMart App (Both VMs)**

```bash
git clone https://github.com/atingupta2006/oci-multi-tier-web-app-ecommerce.git
cd oci-multi-tier-web-app-ecommerce
npm install
```

---

# ⚙️ **4. Configure Environment Variables (.env)**

Copy template:

```bash
cp prd.env .env
```

Edit:

```bash
nano .env
```

### Update this section using values from Terraform:

### **Replace with Terraform Output Values:**

| Variable      | Value from Terraform             | Put in .env |
| ------------- | -------------------------------- | ----------- |
| FRONTEND_URL  | `http://161.118.164.93`          | Yes         |
| CORS_ORIGIN   | `http://161.118.164.93`          | Yes         |
| VITE_API_URL  | `http://161.118.164.93:3000/api` | Yes         |
| SUPABASE vars | Your Supabase project            | Yes         |

### **Your corrected values should look like:**

```
FRONTEND_URL=http://161.118.164.93
CORS_ORIGIN=http://161.118.164.93
VITE_API_URL=http://161.118.164.93:3000/api
```

---

# 🗄 **5. Run Database Migrations (Backend VM Only)**

Go to backend VM on **10.0.2.14**.

### Order:

1️⃣ Destroy DB (optional)

```bash
# Manual SQL run from: supabase/migrations/00000000000000_destroy-db.sql
```

2️⃣ Execute SQL setup

```bash
# Manual SQL run from: supabase/migrations/00000000000001_exec_sql.sql
```

3️⃣ Base schema

```bash
npm run db:init
```

4️⃣ Seed data

```bash
# Manual SQL run from: supabase/migrations/00000000000003_seed.sql
```

5️⃣ Set permissions

```bash
# Manual SQL run from: supabase/migrations/00000000000004_set_permissions.sql
```

---

# 🌐 **6. Start Frontend (Frontend VM)**

Run:

### Disable firewall
```
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

```bash
sudo npm run dev -- --host 0.0.0.0 --port 80
```

Background mode:

```bash
nohup npm run dev -- --host 0.0.0.0 --port 80 &
```

Frontend available at:

```
http://161.118.164.93
```

(Terraform output: **load_balancer_url**)

---

# 🔧 **7. Start Backend (Backend VM)**

Run:

```
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

```
sudo systemctl stop nftables
sudo systemctl disable nftables
sudo sysctl net.ipv4.ip_forward
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
sudo sysctl net.ipv4.ip_forward
```

```bash
npm run dev:server
```

Background mode:

```bash
nohup npm run dev:server &
```

Backend API should work via LB:

```
http://161.118.164.93:3000/api/health
```

---

# 🧪 **8. Validate Deployment**

### Frontend:

Open:

```
http://161.118.164.93
```

### Backend API:

```bash
curl http://161.118.164.93:3000/api/health
```

Expected:

```json
{"ok": true, "count": 0}
```

---

# 🔐 **9. Default Users**

Admin:

```
admin@bharatmart.com
Admin@123
```

Customer:

```
rajesh@example.com
customer123
```

---

# 🛑 **10. Restart/Stop Services**

Find running processes:

```bash
ps aux | grep node
```

Stop:

```bash
kill <PID>
```

Restart:

```bash
nohup npm run dev -- --host 0.0.0.0 --port 80 &
nohup npm run dev:server &
```

---

# 🎯 **Summary of Important Sample Values from Terraform Outputs**

These **must be replaced** each deployment:

| Terraform Output                                                                       | Use In .env                             |
| -------------------------------------------------------------------------------------- | --------------------------------------- |
| **load_balancer_public_ip = 161.118.164.93**                                           | FRONTEND_URL, CORS_ORIGIN, VITE_API_URL |
| **backend_private_ip = 10.0.2.14**                                                     | Only for SSH or debugging, NOT in .env  |
| **frontend_public_ip = 141.148.217.172**                                               | Only for SSH                            |
| **backend_api_url = [http://161.118.164.93:3000/api](http://161.118.164.93:3000/api)** | VITE_API_URL                            |
| **frontend_url = [http://161.118.164.93](http://161.118.164.93)**                      | FRONTEND_URL                            |

