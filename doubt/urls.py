
from django.urls import path
from doubt.views import register_user,login_user,student_dashboard

urlpatterns = [
  path("Registration/",register_user,name='register_user'),
  path("Login_user/",login_user,name='login_user'),
  path("Student_home/",student_dashboard,name='student_dashboard'),
]
