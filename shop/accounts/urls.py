from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("api/sign-in/", views.SignInView.as_view(), name="login"),
    path("api/sign-up/", views.SignUpView.as_view(), name="sign_up"),
    path("api/sign-out/", views.signOut, name="sing_out"),
    path("api/profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "api/profile/password/",
        views.ProfilePasswordChangeView.as_view(),
        name="password",
    ),
    path("api/profile/avatar/", views.AvatarView.as_view(), name="avatar"),
]
