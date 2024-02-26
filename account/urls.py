from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path("login/", views.user_login, name="login"),
    # login logout urls
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # password change url
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done", auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done"),
    # password rest
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("", views.dashboard, name="dashboard"),
]
