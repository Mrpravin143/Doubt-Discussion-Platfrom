import os
import django

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Doubt2Solve.settings')

# Setup Django
django.setup()

from doubt.models import *


alldata = AskDoubts.objects.all().delete()
print(alldata)











