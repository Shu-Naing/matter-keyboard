"""raw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from key.views import save_info_id,chatbot_api,check_device
from django.conf import settings
from django.conf.urls.static import static
from django.views import static as views_static
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/save-device-id/', save_info_id, name='save_info_id'),
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
    path('api/check-device/', check_device, name='check_device'),
]