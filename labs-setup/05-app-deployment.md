# 🚀 **BharatMart Application Deployment on OCI VMs**

Your OCI Terraform environment is now ready with:

* **Frontend VM (public IP)**
* **Backend VM (private IP or optional public IP)**
* **Single public Load Balancer**

  * Port **80** → Frontend
  * Port **3000** → Backend

Now follow the steps below to install and run the BharatMart application **on your OCI virtual machines**.

---

# ✅ **1. Connect to the VMs**

## **1.1 SSH to Frontend VM (Public IP)**

```bash
ssh -i ~/.ssh/id_rsa opc@<frontend_public_ip>
```

## **1.2 SSH to Backend VM**

### If backend is private:

SSH **via frontend VM** (jump box):

```bash
ssh -i ~/.ssh/id_rsa opc@<backend_private_ip>
```

### If backend public IP enabled:

```bash
ssh -i ~/.ssh/id_rsa opc@<backend_public_ip>
```

---

# 📦 **2. Install OS Dependencies (Both VMs)**

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

# 📁 **3. Download BharatMart Application (Both VMs)**

```bash
git clone <repository-url>
cd oci-multi-tier-web-app-ecommerce
npm install
```

---

# ⚙️ **4. Configure Environment Variables (.env file)**

Copy production template:

```bash
cp prd.env .env
```

Edit:

```bash
nano .env
```

Update:

```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
VITE_SUPABASE_URL=...
VITE_SUPABASE_ANON_KEY=...

FRONTEND_URL=http://<load_balancer_public_ip>
CORS_ORIGIN=http://<load_balancer_public_ip>
```

Save + exit.

---

# 🗄 **5. Run Database Migrations (Backend VM Only)**

Run migrations **in order**:

### 5.1 Destroy existing schema (optional)

Manually execute file:

```
supabase/migrations/00000000000000_destroy-db.sql
```

### 5.2 Execute SQL setup

```
supabase/migrations/00000000000001_exec_sql.sql
```

### 5.3 Base schema (automated)

```bash
npm run db:init
```

### 5.4 Seed data

```
supabase/migrations/00000000000003_seed.sql
```

### 5.5 Permissions

```
supabase/migrations/00000000000004_set_permissions.sql
```

---

# 🌐 **6. Start the Frontend (Frontend VM)**

```bash
npm run dev -- --host 0.0.0.0 --port 80
```

To run in background:

```bash
nohup npm run dev -- --host 0.0.0.0 --port 80 &
```

---

# 🔧 **7. Start the Backend API (Backend VM)**

```bash
npm run dev:server
```

To run in background:

```bash
nohup npm run dev:server &
```

Backend listens on:

```
http://<backend_vm_ip>:3000
```

And is automatically reachable through LB:

```
http://<load_balancer_public_ip>:3000/api/health
```

---

# 🧪 **8. Verify Deployment**

## **Frontend Check**

Open browser:

```
http://<load_balancer_public_ip>
```

## **Backend Health Check**

```
curl http://<load_balancer_public_ip>:3000/api/health
```

Expected:

```json
{ "ok": true, "count": 0 }
```

---

# 🔐 **9. Default Test Users**

After seeding:

### Admin

* `admin@bharatmart.com`
* `admin123`

### Customer

* `rajesh@example.com`
* `customer123`

---

# 🛑 **10. Stop or Restart the Services**

If you used `nohup`:

List processes:

```bash
ps aux | grep node
```

Kill:

```bash
kill <pid>
```

Or restart from repo folder:

```bash
nohup npm run dev:server &
nohup npm run dev -- --host 0.0.0.0 --port 80 &
```

---

# 🎯 Summary (Short)

| Component        | VM       | Command                                   |
| ---------------- | -------- | ----------------------------------------- |
| Clone App        | Both     | `git clone ... && npm install`            |
| Configure `.env` | Both     | `cp prd.env .env`                         |
| Run migrations   | Backend  | `npm run db:init` + manual SQL            |
| Start frontend   | Frontend | `npm run dev -- --host 0.0.0.0 --port 80` |
| Start backend    | Backend  | `npm run dev:server`                      |
| Verify           | LB       | `http://LB_IP`, `/api/health`             |

