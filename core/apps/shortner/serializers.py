from rest_framework import serializers
from core.apps.shortner.models import LinkShortner

class LinkShortnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkShortner
        fields = '__all__'
        read_only_fields = ['user', 'clicks', 'created_at']
        
    def validate_short_code(self, value):
        if LinkShortner.filter(short_code=value).exists():
            raise serializers.ValidationError("Short code already exists")
        return value