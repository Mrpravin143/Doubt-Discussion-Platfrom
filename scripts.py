import os
import django

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Doubt2Solve.settings')

# Setup Django
django.setup()

from doubt.models import *



status_Updation = DoubtAnswer.objects.all().order_by('created_at')

# for i in status_Updation:
#     if i.status == True:
#         print("Resolved...✅")
#     else:
#         print("Pending...🔴")

students_count = CustomUser.objects.filter(role='Student').count()

print(students_count)











