from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  # <-- added field

    reset_token = models.UUIDField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
class Question(models.Model):
    Tech_Choice=(
        ('python','Python'),
        ('java','Java'),
        ('mysql','Mysql'),
    )
    Technology=models.CharField(max_length=20,choices=Tech_Choice,default='python')
    question=models.TextField()
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)

    answer=models.CharField(max_length=200)

    def __str__(self):
        return str(self.question)

class Result(models.Model):
    Tech_Choices=(
        ('python','Python'),
        ('java','Java'),
        ('mysql','Mysql'),
    )
    Student_Name=models.CharField(max_length=40)
    Mobile_Number=models.CharField(max_length=15)
    Technology=models.CharField(max_length=30,choices=Tech_Choices)
    Score=models.IntegerField()
    Time_taken=models.IntegerField(help_text="time taken in secons")
    Created_At=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.Score)
