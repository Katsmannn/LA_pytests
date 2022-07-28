
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import UserRoleReadViewSet


router = routers.DefaultRouter()
router.register(r'users/(?P<user_id>\d+)/role', UserRoleReadViewSet, basename='role')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
