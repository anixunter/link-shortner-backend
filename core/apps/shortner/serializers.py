from rest_framework import serializers
from core.apps.shortner.models import LinkShortner

class LinkShortnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkShortner
        fields = '__all__'
        read_only_fields = ['user', 'clicks', 'created_at']
        

class LinkLookUpSerializer(serializers.Serializer):
    original_link = serializers.URLField(read_only=True)