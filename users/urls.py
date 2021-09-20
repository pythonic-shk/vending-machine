from django.urls import path
from .views import UserRegistrationView, UserView, UserChangePwd,\
    UserDeleteView, UserDepositView, UserDepResetView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('register', UserRegistrationView.as_view()),
    path('users/token', obtain_jwt_token),
    path('users/token/refresh', refresh_jwt_token),
    path('users/me', UserView.as_view()),
    path('users/changepwd', UserChangePwd.as_view()),
    path('users/delete', UserDeleteView.as_view()),
    path('users/deposit', UserDepositView.as_view()),
    path('users/reset', UserDepResetView.as_view()),
]