# Steps
### 1. Spin up redpanda broker
`docker compose up -d`

*then set up forwarding to `syslog` topic (rsyslog)*

### 2. Install requirements
```
python3 -m venv venv
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start flask app
python scripts/app.py