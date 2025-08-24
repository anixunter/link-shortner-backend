from django.urls import path
from core.apps.shortner.views import LinkShortnerCreateView, UserLinksListView, RedirectView

urlpatterns = [
    path('create/', LinkShortnerCreateView.as_view(), name='create-link'),
    path('my-links/', UserLinksListView.as_view(), name='user-links'),
    path('<str:short_code>/', RedirectView.as_view(), name='redirect'),
]