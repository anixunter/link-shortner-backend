from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            "password": {"write_only": True},
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exits():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        
        return super().update(instance, validated_data)