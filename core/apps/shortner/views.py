import string
import random
from django.shortcuts import redirect
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.apps.shortner.models import LinkShortner
from core.apps.shortner.serializers import LinkShortnerSerializer


def _generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choice(chars) for _ in range(length))
        if not LinkShortner.objects.filter(short_code=code).exists():
            return code

class LinkShortnerCreateView(generics.CreateAPIView):
    queryset = LinkShortner.objects.all()
    serializer_class = LinkShortnerSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        #generate short code if not provided
        if 'short_code' not in serializer.validated_data or not serializer.validated_data['short_code']:
            serializer.validated_data['short_code'] = _generate_short_code()
        
        #set the user to the current authenticated user
        serializer.validated_data['user'] = request.user
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializers.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLinksListView(generics.ListAPIView):
    serializer_class = LinkShortnerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LinkShortner.objects.filter(user=self.request.user)
    

class RedirectView(APIView):
    def get(self, request, short_code):
        try:
            link = LinkShortner.get(short_code=short_code)
            link.clicks += 1
            link.save()
            return redirect(link.original_link)
        except LinkShortner.DoesNotExist:
            return Response({"error": "Short link not found"}, status=status.HTTP_404_NOT_FOUND)


