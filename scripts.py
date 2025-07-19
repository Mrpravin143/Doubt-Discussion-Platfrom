import os
import django

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Doubt2Solve.settings')

# Setup Django
django.setup()

from doubt.models import  CustomUser

user = CustomUser.objects.all()

if user.role == "admin":
    print()

# from django.contrib.auth import get_user_model

# User = get_user_model()


# print(User)



