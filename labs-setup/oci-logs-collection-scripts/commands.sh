cd
git clone https://github.com/atingupta2006/oci-sre-training-dec-25.git
cd oci-sre-training-dec-25
python3 -m venv ~/venv
source ~/venv/bin/activate
cd labs-setup/oci-logs-collection-scripts/
pip install -r requirements.txt
mv .env.example .env
nohup python3 backend-metrics-to-oci.py > metrics.out 2>&1 &
nohup python3 backend-logs-to-oci.py > backend-logs.out 2>&1 &
nohup python3 frontend-access-logs-to-oci.py > fe-access.out 2>&1 &
nohup python3 frontend-error-logs-to-oci.py > fe-error.out 2>&1 &
ps aux | grep python



pkill -f backend-metrics-to-oci.py

