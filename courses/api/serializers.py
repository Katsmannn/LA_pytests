from rest_framework import serializers

from .models import UserRole

class UserRoleSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'role', 'user']
