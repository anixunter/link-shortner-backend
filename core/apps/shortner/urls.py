from django.urls import path
from core.apps.shortner.views import LinkShortnerCreateView, UserLinksListView

urlpatterns = [
    path('create/', LinkShortnerCreateView.as_view(), name='create-link'),
    path('', UserLinksListView.as_view(), name='user-links'),
]