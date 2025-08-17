from django.urls import path
from doubt.views import *

urlpatterns = [
  path("Registration/",register_user,name='register_user'),
  path("Login_user/",login_user,name='login_user'),
  path("",student_dashboard,name='student_dashboard'),
  path("Ask_Doubts/",ask_doubts, name='ask_doubts'),
  path("logout/",user_logout,name='user_logout'),
  path("Profile/",profile_view,name='profile_view'),
  path("teacher/doubts/",teacher_doubts,name='teacher_doubts'),
  path("teacher/answer/<int:doubt_id>/", answer_doubt, name='answer_doubt'),
  path("student/dashboard/",my_doubts,name="my_doubts")
]
