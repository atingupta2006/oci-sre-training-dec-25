# Health-check function — BharatMart

I've prepared a small OCI Function called `health-check` to run HTTP health checks against one or more endpoints and write a single structured JSON log for each run. It's deliberately simple so you can deploy quickly and integrate logs with OCI (Service Connector Hub or direct Console workflows).

What you get
- `func.py` — function code (Python / FDK)
- `func.yaml` — function settings (runtime, memory, timeout)
- `requirements.txt` — Python dependencies
- `commands.sh` — helper to run local test or `fn invoke`
- `event-rule-monitoring-to-function.json` — example Event Rule JSON (for reference)

Environment (example)
---------------------
Create a `.env` locally or set these with `fn config function`. Example:

```
HEALTH_URLS=http://127.0.0.1:3000/api/health
REQUEST_TIMEOUT=5
RETRIES=1
BACKOFF_SECONDS=1.0
# Optional thresholds:
LATENCY_THRESHOLD_MS=1000
ORDERS_FAILED_THRESHOLD=0
```

Why I built it this way
- No Redis, no Vault, no extra infra in the function itself — keeps it easy to run.
- The function logs a JSON summary that can be routed by Service Connector Hub to Notifications, email, Slack, or other targets.
- You can trigger it on a schedule or from an alarm; alarm → function is a practical automation for SRE workflows.

How I expect you to use it
--------------------------
1. Build the function:
```bash
cd health-check-fn
fn build
```

2. Deploy to your existing Functions Application:
```bash
# replace <app-name> with your Functions Application name
fn deploy --app <app-name>
```

3. Configure runtime settings (persistent):
```bash
fn config function <app-name> health-check HEALTH_URLS "http://<lb-ip>:3000/api/health"
fn config function <app-name> health-check REQUEST_TIMEOUT "5"
fn config function <app-name> health-check RETRIES "1"
fn config function <app-name> health-check BACKOFF_SECONDS "1.0"
fn config function <app-name> health-check LATENCY_THRESHOLD_MS "1000"
fn config function <app-name> health-check ORDERS_FAILED_THRESHOLD "0"
```

4. Run it (manual)
------------------
Open `health-check-fn/commands.sh` and run the commands one by one, replacing placeholders:

- `cd health-check-fn`
- `fn build`
- `fn deploy --app <app-name>`
- `fn config function <app-name> health-check HEALTH_URLS "http://<lb-ip>:3000/api/health"`
- `fn config function <app-name> health-check REQUEST_TIMEOUT "5"`
- `fn config function <app-name> health-check RETRIES "1"`
- `fn config function <app-name> health-check BACKOFF_SECONDS "1.0"`
- `fn config function <app-name> health-check LATENCY_THRESHOLD_MS "1000"`
- `fn config function <app-name> health-check ORDERS_FAILED_THRESHOLD "0"`
- `fn invoke <app-name> health-check`

You should receive a JSON response with `run_id`, `overall_status`, individual `results`, and any metric concerns discovered during the scrape of `/metrics`.

How to wire it into OCI (simple options)
---------------------------------------
- Schedule: create an Events Rule (Schedule) in the Console to call the function periodically.
- Alarm-driven: create a Monitoring Alarm (for example, increased 5xx rate) and configure an Events Rule to invoke this function when the alarm moves to FIRING.
- Logs routing: use Service Connector Hub to route the function's logs (Functions log group) to Notifications, Email, or other sinks.

Notes & tips
------------
- If `fn deploy` fails, check Docker and that `fn` is configured to your OCI tenancy.
- Increase `timeout` in `func.yaml` if you expect long-running checks.
- For private backends, make sure the function has network access (VCN/Private Endpoint).
- This function intentionally avoids pushing custom metrics — use OCI Monitoring or log-based metrics if you want dashboards/alerts.

If you want me to:
- Fill in the `fn config` commands with your real application name and LB IP, I will provide them ready to paste.
- Or I can provide a tiny Console checklist to create the Events Rule for Monitoring → Function.
*** End Patch**"}]}
