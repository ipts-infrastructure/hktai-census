# Nginx GoAccess Docker Setup

A Docker Compose setup demonstrating Nginx load balancing with GoAccess real-time log analysis. This project includes Flask backend services, Nginx reverse proxy with load balancing, and GoAccess for real-time web log analytics.

## 🚀 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## 🛠️ Getting Started

### 1. Clone and Navigate
```bash
git clone https://github.com/ipts-infrastructure/nginx-goaccess-docker.git
cd nginx-goaccess-docker
```

### 2. Start Services
```bash
docker compose up -d
```

### 3. Configure Test Script
Edit `./scripts/send_requests.sh` to configure:
- `REQUEST_URL`: Target endpoint (default: `http://localhost:81/v1/chat/completions`)
- `MODEL_NAME`: Model identifier (default: `qwen/qwen3-vl-4b`)

### 4. Generate Test Traffic
```bash
# Send 20 test requests
./scripts/send_requests.sh 20
```

### 5. Apply Nginx Config Changes (if needed)
```bash
# Restart to apply updated nginx configuration
docker compose restart
```

### 6. View Analytics
Open `./goaccess/report.html` to view the generated GoAccess HTML report.

## 📁 Project Structure

```
├── compose.yaml           # Docker Compose configuration
├── Dockerfile             # Flask app container
├── app.py                 # Simple Flask health check service
├── requirements.txt       # Python dependencies
├── nginx_config/
│   └── nginx.conf        # Nginx load balancer configuration
├── goaccess_config/
│   └── goaccess.conf     # GoAccess log format configuration
├── goaccess/
│   └── report.html       # Generated GoAccess HTML report
├── scripts/
│   ├── send_requests.sh  # Traffic generation script (auto-created)
│   └── example_payload.json
└── logs/                 # Nginx access/error logs (auto-created)
```

## 🚨 Troubleshooting

### Services Won't Start
```bash
# Check port conflicts
sudo netstat -tulpn | grep -E ':(81|7890|5001|5002)'

# View container logs
docker compose logs [service-name]
```

### GoAccess Not Showing Data
```bash
# Check if logs directory exists and has proper permissions
ls -la logs/

# Verify log format in goaccess.conf matches nginx log format
docker exec goaccess cat /etc/goaccess/goaccess.conf
```

### Reset Everything
```bash
docker compose down -v
docker compose up -d
```

## 🔖 References

- [GoAccess Man Page](https://goaccess.io/man) - GoAccess manual page
- [Nginx Load Balancing Guide](https://nginx.org/en/docs/http/load_balancing.html) - Nginx upstream configuration

## 📄 License
