from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re 

class Validator(models.Manager):
    def register(self, first_name, last_name, email, password, confirm):
        errors = []
        if len(first_name) < 2:
            errors.append("Name must be at least 2 characters")
        if len(first_name) < 1:
            errors.append("Name is required")
        if len(last_name) < 2:
            errors.append("Last Name must be at least 2 characters")
        if len(last_name) < 1:
            errors.append("Last Name is required")
        if len(email) < 1:
            errors.append("Email is required")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Email not valid")
        if len(password) < 8:
            errors.append("Password must be 8 characters or more")
        if len(password) < 1:
            errors.append("Password is required")
        if len(confirm) < 1:
            errors.append("Confirm password is required")
        if confirm != password:
            errors.append("Confirm password should match your password")

        response= {
            "errors":errors,
            "valid":True,
            "user":None,
            "id": None
        }

        if len(errors) > 0:
            response["valid"] = False
            response['errors'] = errors
        else:
            response['user'] = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email.lower(),
                password=password,
            )
            matchingEmail = User.objects.filter(email=email)
            response['id'] = matchingEmail[0].id
        return response

    def login(self, email, password):
        errors = []
        
        response = {
            "errors": errors,
            "valid": True,
            "user": None,
            "id": None
        }

        matchingEmail = User.objects.filter(email=email)
        if len(matchingEmail) > 0:
            if password == matchingEmail[0].password:
                response['valid'] = True
                response['id'] = matchingEmail[0].id
            else:
                errors.append("Incorrect password")
        else:
            errors.append("Incorrect email")

        if len(errors) > 0:
            response['errors'] = errors
            response['valid'] = False

        return response

    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors["title"] = "Title must be longer than 3 characters"
        if len(postData['desc']) < 10:
            errors["des"] = "Description should be at least 10 characters"
        if len(postData['location']) < 1:
            errors["location"] = "Location can't be empty"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validator()

class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    location = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="jobs")
    fav_job = models.ForeignKey(User, related_name="favorites", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validator()