from django.contrib import admin
from django.urls import path, include

api_version = "v1"

api_base = f"api/{api_version}"

urlpatterns = [
    path(f'{api_base}/password/', include('password.urls')),
    path(f'{api_base}/organization/', include('organization.urls')),
    path(f'{api_base}/user/', include('user.urls')),
    path(f'admin/', admin.site.urls),
]
