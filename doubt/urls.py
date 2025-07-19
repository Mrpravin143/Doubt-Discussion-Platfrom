
from django.urls import path
from doubt.views import register_user,login_user

urlpatterns = [
  path("Registration/",register_user,name='register_user'),
  path("Login_user/",login_user,name='login_user'),
]
