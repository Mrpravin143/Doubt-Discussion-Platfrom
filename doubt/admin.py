from django.contrib import admin
from doubt.models import *

#Register your models here.


@admin.register(CustomUser)
class CustomUsers(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','role','course','division','year')
    search_fields = ('first_name','last_name','course')
    list_filter = ('role','division','year')

@admin.register(Coordinator)
class Coordinators(admin.ModelAdmin):
    list_display = ('image','name','role')
    
    

@admin.register(DevlopmentTeam)
class DevlopmentTeams(admin.ModelAdmin):
    list_display = ('image','name','role')

    
@admin.register(Features)
class FeaturesOfApp(admin.ModelAdmin):
    list_display = (['name'])
    
@admin.register(AskDoubts)
class AskDoubtsT(admin.ModelAdmin):
    list_display = ('user','doubt_name','doubt_description','teacher_select','subject_select','doubt_image','created_at')
    search_fields = ('teacher_select','subject_select')
    list_filter = ('teacher_select','subject_select')
    
@admin.register(UserProfile)
class UserProfiles(admin.ModelAdmin):
    list_display = ('user','intrest','future_goals','about_me','Skills')
    search_fields = ('Skills','future_goals')
    list_filter = (['Skills'])

@admin.register(DoubtAnswer)
class DoubtAnswerT(admin.ModelAdmin):
    list_display = ('doubt','teacher','answer_text','answer_file','created_at')
    search_fields = ('doubt','teacher','answer_file','created_at')
    list_filter = (['teacher'])
    



