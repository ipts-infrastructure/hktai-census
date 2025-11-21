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

### 5. Configure Load Balancing

#### Change Backend Server IPs
Edit `./nginx_config/nginx.conf` to update the upstream server IPs:

```nginx
upstream lm_studio_grp_1 {
    server 192.168.1.100:1234;  # Update to your server IP
    server 192.168.1.101:8000;  # Add/remove servers as needed
}
```

#### Load Balancing Methods
Uncomment one of these directives in the upstream block:

```nginx
upstream lm_studio_grp_1 {
    # Round Robin (default) - distributes requests evenly
    
    # ip_hash;  # Routes same client IP to same server
    # least_conn;  # Routes to server with fewest active connections
    # random;  # Routes randomly (nginx 1.15.1+)
    
    server 192.168.1.100:1234 weight=3;  # Higher weight = more requests
    server 192.168.1.101:8000 weight=1;
}
```

#### Apply Configuration Changes
```bash
# Test configuration syntax
docker exec nginx nginx -t

# Reload configuration without downtime
docker exec nginx nginx -s reload

# Or restart entire stack
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

## ⚖️ Load Balancing Configuration

### Updating Backend Server IPs

1. **Edit the nginx configuration**:
   ```bash
   nano ./nginx_config/nginx.conf
   ```

2. **Modify the upstream block**:
   ```nginx
   upstream lm_studio_grp_1 {
       server 10.0.1.100:1234;    # Production server 1
       server 10.0.1.101:1234;    # Production server 2
       server 10.0.1.102:8000;    # Backup server
   }
   ```

### Load Balancing Methods

#### Round Robin (Default)
```nginx
upstream lm_studio_grp_1 {
    server 192.168.1.100:1234;
    server 192.168.1.101:8000;
}
```
Distributes requests evenly across all servers.

#### IP Hash
```nginx
upstream lm_studio_grp_1 {
    ip_hash;
    server 192.168.1.100:1234;
    server 192.168.1.101:8000;
}
```
Routes requests from the same client IP to the same server (session persistence).

#### Least Connections
```nginx
upstream lm_studio_grp_1 {
    least_conn;
    server 192.168.1.100:1234;
    server 192.168.1.101:8000;
}
```
Routes to the server with the fewest active connections.

#### Weighted Round Robin
```nginx
upstream lm_studio_grp_1 {
    server 192.168.1.100:1234 weight=3;
    server 192.168.1.101:8000 weight=1;
}
```
Server with weight=3 receives 3x more requests than weight=1.

#### Server Options
```nginx
upstream lm_studio_grp_1 {
    server 192.168.1.100:1234 weight=3 max_fails=2 fail_timeout=30s;
    server 192.168.1.101:8000 backup;  # Only used when primary servers fail
    server 192.168.1.102:8000 down;    # Temporarily disabled
}
```

## 🔖 References

- [GoAccess Man Page](https://goaccess.io/man) - GoAccess manual page
- [Nginx Load Balancing Guide](https://nginx.org/en/docs/http/load_balancing.html) - Nginx upstream configuration
- [Nginx Upstream Module](https://nginx.org/en/docs/http/ngx_http_upstream_module.html) - Detailed upstream configuration

## 📄 License
