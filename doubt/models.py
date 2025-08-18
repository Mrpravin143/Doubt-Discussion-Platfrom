from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from doubt.encryption import encrypt_text, decrypt_text
from django.conf import settings



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    course = models.CharField(max_length=200, null=True, blank=True)
    division = models.CharField(max_length=80, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return f"{self.email} ({self.role})"


class Coordinator(models.Model):
    image = models.ImageField(upload_to='coordinators/',null=True,blank=True)
    name = models.CharField(max_length=100)
    role = models.TextField()
  

class DevlopmentTeam(models.Model):
    image = models.ImageField(upload_to='devlopment_team/',null=True,blank=True)
    name = models.CharField(max_length=100)
    role = models.TextField()

class Features(models.Model):
    name = models.TextField()

class Logo(models.Model):
    logo = models.ImageField(upload_to='main_logo/', null=True,blank=True) 


class AskDoubts(models.Model):
    SUBJECT_CHOICE = (
        ('python','PYTHON'),
        ('Cloud Cmputing','CLOUD COMPUTING'),
        ('Machine Learning','MACHINE LEARNING'),
        ('C','C'),
        ('Emplyebility Skill','EMPLOYBILITY SKILL'),
    )

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    doubt_name = models.CharField(max_length=500)
    doubt_description = models.TextField(null=True,blank=True)
    teacher_select = models.CharField(max_length=200,choices=SUBJECT_CHOICE, blank=True , null=True)
    subject_select = models.CharField(max_length=300)
    doubt_image = models.ImageField(null=True,blank=True,upload_to='doubt_images/')
    created_at = models.DateTimeField(auto_now_add = True)


    def save(self, *args, **kwargs):
        self.doubt_name = encrypt_text(self.doubt_name)
        self.doubt_description = encrypt_text(self.doubt_description)
        super().save(*args, **kwargs)

    def get_decrypted_name(self):
        return decrypt_text(self.doubt_name)

    def get_decrypted_description(self):
        return decrypt_text(self.doubt_description)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    intrest = models.CharField(max_length=500,blank=True,null=True)
    future_goals = models.CharField(max_length=300,blank=True,null=True)
    about_me = models.TextField(max_length=600,blank=True,null=True)
    Skills = models.CharField(max_length=300,blank=True,null=True)


# teacher answer sending....

class DoubtAnswer(models.Model):
    doubt = models.ForeignKey(AskDoubts, on_delete=models.CASCADE, related_name="answers")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    answer_text = models.TextField(blank=True, null=True)
    answer_file = models.FileField(upload_to="answer_files/", blank=True, null=True)
    status = models.BooleanField(default=True ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.teacher.email} for {self.doubt.get_decrypted_name()} {self.status}"





    
