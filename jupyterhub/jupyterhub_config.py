# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

from oauthenticator.google import GoogleOAuthenticator
from oauthenticator.azuread import AzureAdOAuthenticator

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

c.Spawner.start_timeout = 300  # seconds, default is 60

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Allow all signed-up users to login
c.Authenticator.allow_all = True

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = True

# pip oauthenticator
# https://pypi.org/project/oauthenticator/0.10.0/

# Google oauth
# c.JupyterHub.authenticator_class = GoogleOAuthenticator
# c.GoogleOAuthenticator.client_id = 'xxxxxxxxxxxxx.apps.googleusercontent.com'
# c.GoogleOAuthenticator.client_secret = 'xxxxxxxxxxxxxxxxxxxxxx'
# c.GoogleOAuthenticator.oauth_callback_url = 'http://localhost:8000/hub/oauth_callback'

# Azure oauth
# c.JupyterHub.authenticator_class = AzureAdOAuthenticator
# c.AzureAdOAuthenticator.client_id = 'xxxx'
# c.AzureAdOAuthenticator.client_secret = 'xxxx'
# c.AzureAdOAuthenticator.oauth_callback_url = 'https://localhost:8080/hub/oauth_callback'
# c.AzureAdOAuthenticator.tenant_id = 'xxxx'  # Optional, defaults to common
# c.AzureAdOAuthenticator.allow_all = True  # Or restrict with allowed_emails

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]
