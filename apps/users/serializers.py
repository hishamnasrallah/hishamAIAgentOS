from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import HishamOSUser, UserPermission, Role


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ['id', 'permission_name', 'resource_type', 'resource_id', 'granted_at', 'granted_by']
        read_only_fields = ['id', 'granted_at', 'granted_by']


class UserSerializer(serializers.ModelSerializer):
    custom_permissions = UserPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = HishamOSUser
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'avatar', 'preferences', 'ai_token_limit',
            'ai_tokens_used', 'last_token_reset', 'is_active',
            'created_at', 'updated_at', 'custom_permissions'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'ai_tokens_used', 'last_token_reset']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = HishamOSUser
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'role'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = HishamOSUser.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HishamOSUser
        fields = [
            'first_name', 'last_name', 'avatar', 'preferences'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Passwords do not match."})
        return attrs


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HishamOSUser
        fields = [
            'role', 'ai_token_limit', 'is_active'
        ]
