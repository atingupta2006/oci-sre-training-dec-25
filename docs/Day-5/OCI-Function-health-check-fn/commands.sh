1) Change to function directory
   cd health-check-fn

2) Inspect or create local .env

3) Build the function image
   fn build

4) Deploy to your Functions Application
   # replace app-my-func with your Functions Application name
   fn list apps
   fn deploy --app app-my-func

5) Configure runtime variables
   fn config function app-my-func health-check HEALTH_URLS "http://161.118.191.254:3000/api/health"
   fn config function app-my-func health-check REQUEST_TIMEOUT "5"
   fn config function app-my-func health-check RETRIES "1"
   fn config function app-my-func health-check BACKOFF_SECONDS "1.0"
   fn config function app-my-func health-check LATENCY_THRESHOLD_MS "1000"
   fn config function app-my-func health-check ORDERS_FAILED_THRESHOLD "0"

6) Invoke the deployed function
   # replace app-my-func
   fn invoke app-my-func health-check

