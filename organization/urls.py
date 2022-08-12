from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('', viewset=views.OrganizationViewSet, basename='organization')

share_router = routers.DefaultRouter()
share_router.register('', viewset=views.OrgAccessUserViewSet,
                      basename='org-access-user')

password_router = routers.DefaultRouter()
password_router.register(
    '', viewset=views.OrgPasswordViewSet, basename='org-password')


urlpatterns = [
    path('', include(router.urls)),
    path('<int:oid>/members/', include(share_router.urls)),
    path('<int:oid>/passwords/', include(password_router.urls)),
]
