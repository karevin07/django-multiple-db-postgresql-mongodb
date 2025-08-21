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
        'NAME': os.environ.get('POSTGRES_NAME'),
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'postgres',
        'PORT': os.environ.get('POSTGRES_PORT'),
    },
    'mongo_db': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': os.environ.get('MONGO_DATABASE'),
        'CLIENT': {
            'host': f"mongodb://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PASSWORD')}@mongo:27017/{os.environ.get('MONGO_DATABASE')}?authSource=admin",
            'username': os.environ.get('MONGO_USER'),
            'password': os.environ.get('MONGO_PASSWORD'),
            'authSource': 'admin',
        },
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
