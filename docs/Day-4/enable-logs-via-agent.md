# OCI UMA – NGINX Access Log Ingestion Runbook

## 1. Enable UMA on a Fresh Oracle Linux 8 Machine

```bash
sudo dnf install -y oracle-cloud-agent oracle-cloud-agent-plugins-all
sudo systemctl enable --now unified-monitoring-agent
```

Verify UMA is running:

```bash
systemctl status unified-monitoring-agent
```

## 2. Install and Configure NGINX

```bash
sudo dnf install -y nginx
sudo systemctl enable --now nginx
```

Verify logs exist:

```bash
ls -l /var/log/nginx/access.log
```

Ensure UMA can read logs:

```bash
sudo chmod 644 /var/log/nginx/access.log
```

## 3. Create OCI Agent Configuration (No Parser)

In OCI Console → Logging → Agent Configurations → Create:

**General:**

* Name: `ng-access-logs`
* Compartment: your working compartment

**Host Group:**

* Type: Dynamic Group
* Select your DG

**Log Input:**

* Input type: Log path
* Input name: `ng-access-logs`
* File paths: `/var/log/nginx/access.log`
* Parser: **None** (no parsing)

**Destination:**

* Log Group: `lg-nginx-access-log`
* Log Name: `nginx-access-log`

Click **Create**.

## 4. Restart UMA to Force Refresh

```bash
sudo systemctl restart unified-monitoring-agent
sleep 5
```

Check assignment and startup:

```bash
tail -n 50 /var/log/unified-monitoring-agent/unified-monitoring-agent.log
```

Look for:

* `using authentication principal auto`
* `adding source type="tail"`
* `following tail of /var/log/nginx/access.log`
* `put_logs request`

## 5. Generate Test Traffic

```bash
while true; do curl -A "UMA-Test" http://127.0.0.1/ >/dev/null 2>&1; sleep 1; done
```

Check NGINX logs update:

```bash
tail /var/log/nginx/access.log
```

## 6. Verify UMA is Actively Tailing

```bash
sudo lsof /var/log/nginx/access.log | grep unified-monitoring || echo "UMA_NOT_TAILING"
```

If UMA_NOT_TAILING prints, agent config is not applied.

## 7. Confirm Logs Sent to OCI

```bash
sudo grep "put_logs request" /var/log/unified-monitoring-agent/unified-monitoring-agent.log
```

A valid entry confirms transmission.

## 8. Troubleshooting Checklist

### A. Dynamic Group Membership

Confirm instance OCID appears in DG evaluation:

```bash
oci iam dynamic-group get --dynamic-group-id <DG_OCID> --query "data" --output table
```

### B. UMA Feature Enabled

```bash
curl -s http://169.254.169.254/opc/v1/instance/ | grep -A5 "Custom Logs Monitoring"
```

Should show:

```
"desiredState": "ENABLED"
```

### C. Agent Downloading Assignment

Check for missing assignment:

```bash
grep "downloading assignment" /var/log/unified-monitoring-agent/unified-monitoring-agent.log
```

### D. File Permission Issues

```bash
sudo ls -l /var/log/nginx/access.log
```

Permissions must allow UMA read access.

### E. Verify UMA Tail Block

Search for any errors:

```bash
sudo egrep -i "error|fail|nginx|access.log" /var/log/unified-monitoring-agent/unified-monitoring-agent.log
```

### F. Confirm UMA Config Is Applied Locally

```bash
sudo grep -R "/var/log/nginx/access.log" /etc/unified-monitoring-agent
```

If no match → config never downloaded.

### G. Restart UMA Cleanly

```bash
sudo systemctl restart unified-monitoring-agent
```

Wait 5 seconds and re-check logs.
