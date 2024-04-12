from rest_framework import serializers
from .models import Profile, Avatar


class FileUploadAvatarSerializer(serializers.Serializer):
    file = serializers.ListSerializer(child=serializers.CharField())


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("password",)

    def update(self, instance, validated_data):
        password = validated_data.pop("newPassword", None)
        instance.set_password(password)
        return super().update(instance, validated_data)
