# Jupyterhub & notebook Docker Setup

This repository contains Docker configurations for running Jupyter Notebook and JupyterHub. It includes two main setups:

1. **JupyterHub** - A multi-user Jupyter notebook platform with authentication

## 🚀 Prerequisites

- **Docker** (version 20.10 or later)
- **Docker Compose** (version 2.0 or later)

## 🛠️ Getting Started

**JupyterHub (Multi-User)**

- **Step 1 — Change to the JupyterHub directory:**

```bash
cd jupyterhub
```

- **Step 2 — Choose the Notebook image (Python version)**

Open `docker-compose.yml` and set the `DOCKER_NOTEBOOK_IMAGE` you want JupyterHub to spawn for notebook servers. Example options (uncomment one):

```yaml
# JupyterHub will spawn this Notebook image for users
# https://quay.io/repository/jupyter/base-notebook?tab=tags&tag=latest
# DOCKER_NOTEBOOK_IMAGE: quay.io/jupyter/base-notebook:latest
# DOCKER_NOTEBOOK_IMAGE: quay.io/jupyter/base-notebook:python-3.11
DOCKER_NOTEBOOK_IMAGE: quay.io/jupyter/base-notebook:python-3.12
```

Recommendation: use the latest stable `base-notebook` tag that matches your project Python requirement (e.g., `python-3.12`).

- **Step 3 — Start JupyterHub:**

```bash
docker compose up -d
```

- **Step 4 — Access the UI:**

Open a browser to `http://localhost:8000` (adjust host/port if changed in `docker-compose.yml`).

- **Step 5 — Admin user and sign-up:**

By default you can allow local sign-up or predefine an admin via environment variables in `docker-compose.yml`:

```yaml
environment:
  # This username will be a JupyterHub admin
  JUPYTERHUB_ADMIN: admin
```

Create an account or sign in using the admin username above. The first user who signs up with the `JUPYTERHUB_ADMIN` username becomes an admin.

- **Useful commands**

```bash
# View logs for the JupyterHub service
cd jupyterhub && docker compose logs -f

# Restart after changing config (e.g., jupyterhub_config.py or docker-compose.yml)
cd jupyterhub && docker compose restart

# Stop and remove volumes (reset state)
docker compose down -v
```

## 🔐 Authentication Methods

JupyterHub supports multiple authentication methods. Edit `jupyterhub_config.py` to configure:

### Native Authenticator (Default)
- Users can create accounts directly
- Open signup enabled by default
- Admin user: `admin` (configurable via `JUPYTERHUB_ADMIN` in docker-compose.yml)
- First user to sign up with the admin username automatically becomes admin

### Google OAuth
Uncomment and configure in `jupyterhub_config.py`:
```python
c.JupyterHub.authenticator_class = GoogleOAuthenticator
c.GoogleOAuthenticator.client_id = '1234567890-abcdefg.apps.googleusercontent.com'
c.GoogleOAuthenticator.client_secret = 'XyZ1234567890abcdefgHIJKL='
c.GoogleOAuthenticator.oauth_callback_url = 'http://localhost:8000/hub/oauth_callback'
```

### Azure AD OAuth
Uncomment and configure in `jupyterhub_config.py`:
```python
c.JupyterHub.authenticator_class = AzureAdOAuthenticator
c.AzureAdOAuthenticator.client_id = '12345678-abcd-1234-abcd-1234567890ab'
c.AzureAdOAuthenticator.client_secret = 'abcD3fGh1JKlMnoPqRsTuVwXyZ1234567890='
c.AzureAdOAuthenticator.tenant_id = '87654321-dcba-4321-dcba-0987654321ba'
c.AzureAdOAuthenticator.oauth_callback_url = 'https://localhost:8080/hub/oauth_callback'
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
- [ldapauthenticator](https://github.com/jupyterhub/ldapauthenticator) - LDAP Authenticator Plugin for Jupyter
## 📄 License
