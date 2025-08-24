import string
import random
from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.shortner.models import LinkShortner
from core.apps.shortner.serializers import LinkShortnerSerializer


def _generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choice(chars) for _ in range(length))
        if not LinkShortner.objects.filter(short_code=code).exists():
            return code

class LinkShortnerViewSet(viewsets.ModelViewSet):
    serializer_class = LinkShortnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LinkShortner.objects.filter(user=self.request.user).select_related('user')
    
    def perform_create(self, serializer):
        short_code = serializer.validated_data.get('short_code')
        if not short_code:
            short_code = _generate_short_code()
        
        serializer.save(user=self.request.user, short_code=short_code)
    

class RedirectView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, short_code):
        try:
            link = get_object_or_404(LinkShortner, short_code=short_code)
            link.clicks += 1
            link.save(update_fields=['clicks'])
            return redirect(link.original_link)
        except LinkShortner.DoesNotExist:
            return Response({"error": "Short link not found"}, status=status.HTTP_404_NOT_FOUND)


