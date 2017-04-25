from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, info):
        errors= []
        # print info['email']
        users = User.objects.filter(email=info['email'])
        # print users
        if not users:
            errors.append("Invalid Email")
        else:
            userpass=User.objects.filter(email=info['email'])
            users1 = User.objects.filter(email=info['email'], password=bcrypt.hashpw(info['password'].encode(), userpass[0].password.encode()))
            # print users1
            if not users1:
                errors.append("Login Invalid")

        return errors

    def register(self, info):
        errors=[]

        #Validate First Name
        if len(info['first_name']) < 2 or not info['first_name'].isalpha():
            errors.append('First name is not valid')
        #Validate Last Name
        if len(info['last_name']) < 2 or not info['last_name'].isalpha():
            errors.append('Last name is not valid')
        #Validate Email
        if not EMAIL_REGEX.match(info['email']):
            errors.append('Email is not valid')
        #Validate password
        if len(info['password']) < 8:
            errors.append('Password must be more than 8 characters')
        #Validate password against confirm_password
        if info['password'] != info['confirm_password']:
            errors.append('Password must match confirm password')

        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Secret(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="secrets")
    like = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
