from django.urls import path
from doubt.views import *

urlpatterns = [
  path("Registration/",register_user,name='register_user'),
  path("Login_user/",login_user,name='login_user'),
  path("Student_home/",student_dashboard,name='student_dashboard'),
  path("Ask_Doubts/",ask_doubts, name='ask_doubts'),
  path("logout/",user_logout,name='user_logout'),
]
