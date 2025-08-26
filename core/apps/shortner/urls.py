from django.urls import path
from rest_framework.routers import DefaultRouter
from core.apps.shortner.views import LinkShortnerViewSet, LinkLookUpView

router = DefaultRouter()

router.register('', LinkShortnerViewSet, basename='link')

urlpatterns = router.urls + [path("lookup/<str:short_code>/", LinkLookUpView.as_view(), name="link-look-up"),]