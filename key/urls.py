from django.urls import path
from myapp.views import save_device_id

urlpatterns = [
    path('api/save-device-id/', save_device_id, name='save_device_id'),
]
