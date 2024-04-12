import datetime
import os
from django.conf import settings
from .models import Profile, Avatar
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    ProfileSerializer,
    ChangePasswordSerializer,
)
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

User = get_user_model()


class SignInView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)
        # cart = c.Cart(request)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = Profile.objects.create_user(username=username, password=password)
            user.first_name = name
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(id=request.user.id)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(id=request.user.id)
        try:
            profile_with_email = Profile.objects.get(email=request.data["email"])
            if profile_with_email == profile:
                raise Exception
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(username=request.user)
        if (
            user.check_password(request.data.pop("currentPassword", None))
            and "newPassword" in request.data
        ):
            serializer = ChangePasswordSerializer(user)
            serializer.update(instance=user, validated_data=request.data)
            return JsonResponse(serializer.data, safe=False)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def valid_type_image(file):
    name = file.name
    if name[-3:] == "png" or name[-3:] == "jpg" or name[-4:] == "jpeg":
        return True
    else:
        return False


def handle_uploaded_avatar(f):
    str_f = str(f)
    path_upload = os.path.join(
        settings.BASE_DIR, settings.UPLOAD_DIR, "accounts/avatars/user_avatars/"
    )
    if str_f in os.listdir(path_upload):
        str_f = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M") + str_f
    path_for_src = "accounts/avatars/user_avatars/" + str_f
    with open(path_upload + str_f, "wb+") as destination:
        for chunk in f:
            destination.write(chunk)
    return path_for_src


class AvatarView(APIView):
    def post(self, request):
        user = User.objects.get(username=request.user)
        file = request.FILES["avatar"]
        if valid_type_image(file):
            path = handle_uploaded_avatar(file)
            avatar = Avatar.objects.create(src=path, alt="Avatar")
            user.avatar = avatar
            user.save()
            return HttpResponse(status=200)
        else:
            return Response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
