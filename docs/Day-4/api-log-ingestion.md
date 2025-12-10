# 1. Machine Preparation (Oracle Linux 8)

Install UMA (Unified Monitoring Agent) and plugins:

```bash
sudo dnf install -y oracle-cloud-agent oracle-cloud-agent-plugins-all
sudo systemctl enable --now unified-monitoring-agent
```

Verify UMA is active:

```bash
systemctl status unified-monitoring-agent
```

Ensure log directory exists:

```bash
sudo ls -l /opt/bharatmart/logs/api.log
```

If permission issues occur:

```bash
sudo chmod 644 /opt/bharatmart/logs/api.log
```

---

# 2. Dynamic Group Setup (Required for UMA Authorization)

Navigate to:

**Identity & Security → Dynamic Groups → Create / Edit Dynamic Group**

Use this exact rule:

```
Any {
  instance.compartment.id = "<COMPARTMENT_OCID>",
  instance.pool.id = "<INSTANCE_POOL_OCID>",
  instance.id = "<INSTANCE_OCID>"
}
```

This ensures UMA can authenticate using **instance principals** on both standalone and pool-based instances.

---

# 3. Policy Setup (Must Allow Log Ingestion)

In **Policies**, add:

```
Allow dynamic-group <DG_NAME> to use log-content in tenancy
Allow dynamic-group <DG_NAME> to read log-groups in tenancy
Allow dynamic-group <DG_NAME> to read log-content in tenancy
```

---

# 4. Create UMA Agent Configuration (Log Path Input)

Navigate:

**Observability & Management → Logging → Agent Configurations → Create Configuration**

### Configuration Values:

**Input Type:** `Log path`

**Input Name:** `bharatmart-api-source`

**File Paths:**

```
/opt/bharatmart/logs/api.log
```

**Parser:** `JSON`

### Event Time Settings (IMPORTANT)

```
Estimate event time = False
Keep time key       = True
Time key            = timestamp
Timeout             = 0 (or blank)
```

### Null Field Settings

```
Replace empty string as null = False
Null value pattern           = (blank)
```

### Destination

* Choose **Log Group**
* Provide **Log Name**, e.g., `bharatmart-api-log`

Save configuration.

UMA will now download the configuration automatically.

---

# 5. Restart UMA (Force Assignment Refresh)

```bash
sudo systemctl restart unified-monitoring-agent
sleep 3
sudo tail -n 50 /var/log/unified-monitoring-agent/unified-monitoring-agent.log
```

You should see:

```
downloading assignment
applying unified agent configuration
following tail of /opt/bharatmart/logs/api.log
put_logs request
```

---

# 6. Confirm Log Ingestion in OCI

### Log Explorer

Go to:

```
Observability → Logging → Log Groups → <Your Log Group> → Log Stream
```

Run a query for last 1 hour.

### Live Tail (Real-Time Validation)

Append a test entry:

```bash
echo '{"test":"uma"}' | sudo tee -a /opt/bharatmart/logs/api.log
```

Live Tail should show this immediately.

---

# 7. Troubleshooting Guide

## 7.1 UMA Not Downloading Assignment

Check UMA logs:

```bash
sudo tail -n 100 /var/log/unified-monitoring-agent/unified-monitoring-agent.log
```

Search for errors:

```bash
sudo egrep -i "error|fail|assignment|unauth" /var/log/unified-monitoring-agent/unified-monitoring-agent.log
```

If you see:

```
Config file does not exist. No UmaSource found.
```

This means **agent configuration has not been applied**.

Fix:

* Recheck Dynamic Group rules
* Ensure policies are correct
* Restart UMA again

---

## 7.2 Confirm Instance Principal Access

```bash
oci --auth instance_principal iam region list
```

If it returns regions → instance principal works.

---

## 7.3 Check Metadata (Instance Pool Indicators)

```bash
curl -s http://169.254.169.254/opc/v1/instance/ | grep -A5 instancePool
```

This confirms the instance belongs to an **instance pool** and must use `instance.pool.id` in the DG rule.

---

## 7.4 Check if UMA Is Tailing the File

```bash
sudo lsof /opt/bharatmart/logs/api.log | grep unified
```
