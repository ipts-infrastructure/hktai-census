# Jupyterhub & notebook Docker Setup

This repository contains Docker configurations for running Jupyter Notebook and JupyterHub. It includes two main setups:

1. **JupyterHub** - A multi-user Jupyter notebook platform with authentication

## 🚀 Prerequisites

- **Docker** (version 20.10 or later)
- **Docker Compose** (version 2.0 or later)

## 🛠️ Getting Started

### JupyterHub (Multi User)

1. Navigate to the jupyterhub directory:
   ```bash
   cd jupyterhub
   ```

2. Start JupyterHub:
   ```bash
   docker compose up -d
   ```

3. Access JupyterHub at `http://localhost:8000`
4. Create an account or login (admin user: `hktdev`)

## 🔐 Authentication Methods

JupyterHub supports multiple authentication methods. Edit `jupyterhub_config.py` to configure:

### Native Authenticator (Default)
- Users can create accounts directly
- Open signup enabled by default
- Admin user: `hktdev` (configurable via `JUPYTERHUB_ADMIN` in docker-compose.yml)
- First user to sign up with the admin username automatically becomes admin

### Google OAuth
Uncomment and configure in `jupyterhub_config.py`:
```python
c.JupyterHub.authenticator_class = GoogleOAuthenticator
c.GoogleOAuthenticator.client_id = 'your-client-id'
c.GoogleOAuthenticator.client_secret = 'your-client-secret'
```

### Azure AD OAuth
Uncomment and configure in `jupyterhub_config.py`:
```python
c.JupyterHub.authenticator_class = AzureAdOAuthenticator
c.AzureAdOAuthenticator.client_id = 'your-client-id'
c.AzureAdOAuthenticator.client_secret = 'your-client-secret'
c.AzureAdOAuthenticator.tenant_id = 'your-tenant-id'
```

**Apply Configuration Changes:**
After modifying `jupyterhub_config.py`, restart JupyterHub:
```bash
cd jupyterhub && docker compose restart
```

## 🚨 Troubleshooting

### Common Issues

- **Port conflicts**: Ensure ports 8889 (Jupyter) and 8000 (JupyterHub) are available
- **Docker socket permission**: JupyterHub needs access to `/var/run/docker.sock`
- **Container startup timeout**: Increase `start_timeout` in jupyterhub_config.py if needed
- **Volume permissions**: Check that Docker volumes have proper read/write permissions

### Logs

```bash
# View JupyterHub logs
cd jupyterhub && docker compose logs -f
```

### Reset Everything
```bash
docker compose down -v
docker compose up -d
```

## 🔖 References

- [JupyterHub Documentation](https://jupyterhub.readthedocs.io/) - JupyterHub setup and configuration
- [Jupyter Base Notebook Image](https://quay.io/repository/jupyter/base-notebook?tab=tags&tag=latest) - Official Jupyter base notebook Docker image repository
- [JupyterHub Docker Deployment](https://github.com/jupyterhub/jupyterhub-deploy-docker) - Reference deployment of JupyterHub with Docker

## 📄 License
