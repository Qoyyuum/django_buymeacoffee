from django.urls import path
from .api import api

app_name = 'buymeacoffee'

urlpatterns = [
    path('', api.urls),  # This includes all django-ninja API endpoints
]
