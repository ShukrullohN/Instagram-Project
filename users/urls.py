
from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    path('register/', SignUpCreateAPIView.as_view(), name='register'),
    path('register/reset/', SignUpCreateAPIView.as_view(), name='register'),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
    path('update/', UpdateUserAPIView.as_view(), name='update'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset'),
    path('avatar/', ChangeUserAvatarView.as_view(), name='avatar'),

]
