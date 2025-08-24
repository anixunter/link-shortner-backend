from django.urls import path
from rest_framework.routers import DefaultRouter
from core.apps.common.views import UserViewSet

router = DefaultRouter()

router.register("", UserViewSet, basename="user")

urlpatterns = router.urls

