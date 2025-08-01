from django.contrib import admin
from doubt.models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Coordinator)
admin.site.register(DevlopmentTeam)
admin.site.register(Features)
admin.site.register(AskDoubts)

