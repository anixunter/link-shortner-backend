from django.urls import path
from rest_framework.routers import DefaultRouter
from core.apps.shortner.views import LinkShortnerViewSet

router = DefaultRouter()

router.register('', LinkShortnerViewSet, basename='link')

urlpatterns = router.urls