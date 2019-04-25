from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "password", "username", "email", "is_active", "is_staff")

    # 重写serializer的create方法，该方法将在serializer.save()时被调用，此处为直接注册用户
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
