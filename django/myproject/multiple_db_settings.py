from .settings import *
import os

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append("example_user")
INSTALLED_APPS.append("example_app")

DATABASES = {
    'default': {
        'NAME': 'user_data',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'postgres',
        'POST': '5432',
    },
    'mongo_db': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': True,
        'USER': os.environ.get('MONGO_USER'),
        'NAME': 'app_data',
        'CLIENT': {
            'host': 'mongo',
            'port': 27017,
            'username': os.environ.get('MONGO_USER'),
            'password': os.environ.get('MONGO_PASSWORD'),
            'authMechanism': 'SCRAM-SHA-1'
        },
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propagate': False,
                }
            },
        },
    }
}


DATABASE_APPS_MAPPING = {
    'example_user': 'default',
    'example_app': 'mongo_db'
}

DATABASE_ROUTERS = ['myproject.routing.MyDBRouter']
