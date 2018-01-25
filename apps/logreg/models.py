from __future__ import unicode_literals

from django.db import models
import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class RegistrationManager(models.Manager):

    def regvalidator(self, first_name, last_name, email, password, confirm):
        errors = []
        if len(first_name) < 1 or not first_name.isalpha():
            errors.append("Your first name cannot be blank and may only be letters.")
        if len(last_name) < 1 or not last_name.isalpha():
            errors.append("Your last name cannot be blank and may only be letters.")
        if len(email) < 1:
            errors.append("Your email cannot be blank.")
        elif not EMAIL_REGEX.match(email):
            errors.append("Your email must be a valid email.")
        elif User.objects.filter(email = email).exists():
			errors.append("This email is already in use.")
        if len(password) < 8:
            errors.append("Your password must be at least 8 characters long.")
        if password != confirm:
            errors.append("Your confirmation password must match your password.")
        return {'errors': errors}
        
    def bcryptor(self, password):
        hashword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return {'pwhash': hashword}
        
    def logvalidator(self, email, password):
        errors = []
        # test = User.objects.filter(email = email )
        # print test['email']

        print email
        print password
        try:
            user = User.objects.get(email = email)
            print user

            if bcrypt.hashpw(password.encode('utf8'), user.pwhash.encode('utf8')) == user.pwhash.encode('utf8'):
                return {'user': user, 'errors': errors}
            errors.append("Incorrect password.")
        except:
            errors.append("Unrecognized email address.")
        return {'errors': errors}
        
    def passvalidator(self, id, password, new, confirm):
    	errors = []
    	if new != confirm:
    		errors.append("Confirmation does not match new password.")
    	if len(new) < 8:
            errors.append("Your password must be at least 8 characters long.")
    	try:
            user = User.objects.get(id = id)
            print user

            if bcrypt.hashpw(password.encode('utf8'), user.pwhash.encode('utf8')) != user.pwhash.encode('utf8'):
            	errors.append("Incorrect old password.")
        except:
        	errors.append("User not found.")
        return {'errors': errors}
        
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    title = models.CharField(max_length = 255)
    gender = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    description = models.CharField(max_length=1000)
    pwhash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RegistrationManager()

class Admin(models.Model):
    users = models.OneToOneField(User)
    privilege_level = models.IntegerField()
