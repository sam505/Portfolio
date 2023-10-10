"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import (handler404, handler403, handler400, handler500)


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('api-path/', include('rest_framework.urls')),
    path('', include('user_interface.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'user_interface.views.page_not_found_view'
handler403 = 'user_interface.views.custom_permission_denied_view'
handler400 = 'user_interface.views.custom_bad_request_view'
handler500 = 'user_interface.views.custom_error_view'