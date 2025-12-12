import os
import json
import time
import logging
from datetime import datetime
import requests
from fdk import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration from environment
HEALTH_URLS = os.getenv("HEALTH_URLS", "http://localhost:3000/api/health")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "5"))
RETRIES = int(os.getenv("RETRIES", "1"))
BACKOFF_SECONDS = float(os.getenv("BACKOFF_SECONDS", "1.0"))
# Thresholds for metric concerns (defaults)
LATENCY_THRESHOLD_MS = int(os.getenv("LATENCY_THRESHOLD_MS", "1000"))
ORDERS_FAILED_THRESHOLD = int(os.getenv("ORDERS_FAILED_THRESHOLD", "0"))

def http_check(url: str):
    attempts = 0
    last_err = None
    while attempts <= RETRIES:
        try:
            t0 = time.time()
            r = requests.get(url, timeout=REQUEST_TIMEOUT)
            latency_ms = int((time.time() - t0) * 1000)
            return {
                "target": url,
                "status": "healthy" if r.status_code == 200 else "unhealthy",
                "status_code": r.status_code,
                "latency_ms": latency_ms,
                "attempts": attempts + 1,
            }
        except Exception as exc:
            last_err = str(exc)
            attempts += 1
            time.sleep(BACKOFF_SECONDS * attempts)
    return {"target": url, "status": "error", "error": last_err, "attempts": attempts}

def parse_metrics(text: str):
    """
    Very small Prometheus text format parser for scalar metrics.
    Returns a dict metric -> float (last seen value).
    """
    metrics = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # split by whitespace, last token is value
        parts = line.split()
        if len(parts) < 2:
            continue
        name_and_labels = parts[0]
        # metric name might have labels like metric{...}
        name = name_and_labels.split("{", 1)[0]
        try:
            val = float(parts[-1])
        except Exception:
            continue
        metrics[name] = val
    return metrics

def metrics_check(base_url: str):
    """
    Try to fetch /metrics from base_url host.
    Returns parsed metrics and simple concerns list.
    """
    concerns = []
    metrics = {}
    try:
        # build metrics endpoint intelligently
        if base_url.endswith("/"):
            metrics_url = base_url + "metrics"
        else:
            metrics_url = base_url + "/metrics"
        r = requests.get(metrics_url, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            metrics = parse_metrics(r.text)
            # compute simple latency if sum/count present
            sum_name = "http_request_duration_seconds_sum"
            count_name = "http_request_duration_seconds_count"
            if sum_name in metrics and count_name in metrics and metrics[count_name] > 0:
                avg_sec = metrics[sum_name] / metrics[count_name]
                avg_ms = int(avg_sec * 1000)
                if avg_ms > LATENCY_THRESHOLD_MS:
                    concerns.append(f"avg_request_latency_ms={avg_ms} exceeds {LATENCY_THRESHOLD_MS}")
            # check orders_failed_total
            if "orders_failed_total" in metrics and metrics["orders_failed_total"] > ORDERS_FAILED_THRESHOLD:
                concerns.append(f"orders_failed_total={int(metrics['orders_failed_total'])} > {ORDERS_FAILED_THRESHOLD}")
    except Exception as e:
        concerns.append(f"metrics_fetch_error:{str(e)}")
    return metrics, concerns

def handler(ctx, data=None):
    started_at = datetime.utcnow().isoformat() + "Z"
    run_id = f"run-{int(time.time())}"
    urls = [u.strip() for u in HEALTH_URLS.split(",") if u.strip()]
    results = []
    overall = "ok"
    metric_concerns = []
    run_start = time.time()

    for u in urls:
        http_res = http_check(u)
        metrics, concerns = metrics_check(u)
        if http_res.get("status") != "healthy" or concerns:
            overall = "degraded" if overall == "ok" else overall
        results.append({"http": http_res, "metrics_summary": concerns})
        metric_concerns.extend(concerns)

    duration_ms = int((time.time() - run_start) * 1000)
    payload = {
        "run_id": run_id,
        "timestamp": started_at,
        "duration_ms": duration_ms,
        "overall_status": overall,
        "results": results,
    }

    # Emit structured JSON log (Functions captures stdout)
    logger.info(json.dumps(payload))

    return response.Response(
        ctx,
        response_data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )


