"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=https;AccountName=cs1100320035ba9d3f6;AccountKey=fvpcYUArfJNJz5wZF3ws73TSOS/+DYyvnuhsPNsSwLy1IJitkRodBuNWWau9YeaghPzfh6PXm/Yj+AStVmXmOw==;EndpointSuffix=core.windows.net'
os.environ['AZURE_CONTAINER_NAME'] = 'test'