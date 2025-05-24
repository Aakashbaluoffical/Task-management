from rest_framework import serializers
from core.models.user_models import User
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = ['id', 'username', 'password','role', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError({"error": "Password must be at least 8 characters long."}, status=400)
        return value

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError({"error": "username is required."}, status=400)
        
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError({"error": "username already exists."}, status=400)
        return value

    def validate_role(self, value):
        request = self.context.get('request')
        method = request.method if request else None

        if value not in ['admin', 'user', 'superadmin']:
            raise serializers.ValidationError({"error": "Invalid role."}, status=400)
        if value == 'superadmin':
            raise serializers.ValidationError({"error": "Only superadmins can create users."}, status=400)
        if value == 'admin' and self.context['request'].user.role != 'superadmin':
            raise serializers.ValidationError({"error": "Only superadmins can create admins."}, status=400)
        
        

        return value
    


    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # hash password manually
        return super().create(validated_data)