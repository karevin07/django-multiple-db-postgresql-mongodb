from .settings import *
import os
import django_mongodb_backend

import jupyterlab

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append("example_user")
INSTALLED_APPS.append("example_app")
INSTALLED_APPS.append("django_extensions")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_NAME', default=None),
        'USER': env('POSTGRES_USER', default=None),
        'PASSWORD': env('POSTGRES_PASSWORD', default=None),
        # Defaults to the Docker Compose service name; override with POSTGRES_HOST
        # (e.g. 127.0.0.1) when running Django outside Compose.
        'HOST': env('POSTGRES_HOST', default='postgres'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    },
    'mongo_db': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': env('MONGO_DATABASE', default=None),
        'HOST': env('MONGO_HOST', default='mongo'),
        'PORT': env.int('MONGO_PORT', default=27017),
        'USER': env('MONGO_ROOT_USER', default=None),
        'PASSWORD': env('MONGO_ROOT_PASSWORD', default=None),
        'AUTH_SOURCE': 'admin',
    },
}


DATABASE_APPS_MAPPING = {
    'admin': 'default',
    'auth': 'default',
    'contenttypes': 'default',
    'sessions': 'default',
    'example_user': 'default',
    'example_app': 'mongo_db',
}

DATABASE_ROUTERS = ['myproject.routing.MyDBRouter']

notebook_default_url = '/lab'

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
    '--notebook-dir', '/home/workspace/notebooks',
    '--NotebookApp.default_url', notebook_default_url,
    '--allow-root',
    '--no-browser',
]
IPYTHON_KERNEL_DISPLAY_NAME = 'Django Kernel'
