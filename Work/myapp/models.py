from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Login(AbstractUser):
    email = models.EmailField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)
    
class Register(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, upload_to="profile")
    Confirm_password = models.CharField(max_length=100, null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    
class Questions(models.Model):
    question=models.CharField(max_length=100, null=True)
    uid=models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True, null=True)
    
class Answers(models.Model):
    qid=models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)
    uid=models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True, null=True)
    answers=models.CharField(max_length=500,null=True)
    like=models.IntegerField(null=True,default="0")
    
    
class Likes(models.Model):
    question_id=models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)
    user_id=models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    answer_id=models.ForeignKey(Answers, on_delete=models.CASCADE, null=True)
    likes=models.CharField(max_length=500,null=True,default=0)