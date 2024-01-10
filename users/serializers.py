from rest_framework import serializers

from django.contrib.auth import authenticate
from django.utils import timezone

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("유저가 존재합니다. 다른 계정명을 사용해주세요.")

        user = User.objects.create_user(username=username, password=password)

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)

    # def validate(self, data):
    #     username = data.get("username", None)
    #     password = data.get("password", None)

    #     if username is None:
    #         raise serializers.ValidationError("username을 입력해주세요.")

    #     if password is None:
    #         raise serializers.ValidationError("password를 입력해주세요.")

    #     user = authenticate(username=username, password=password)

    #     if user is None:
    #         raise serializers.ValidationError("해당 유저를 찾을 수 없습니다.")

    #     if not user.is_active:
    #         raise serializers.ValidationError("해당 유저는 비활성화되었습니다.")

    #     user.last_login = timezone.now()
    #     user.save(update_fields=["last_login"])

    #     return {"username": user.username, "last_login": user.last_login}
