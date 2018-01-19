from __future__ import unicode_literals

from django.db import models
from ..logreg.models import User
# Create your models here.

class Board(models.Model):
	header = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Post(models.Model):
	text = models.CharField(max_length=255)
	poster = models.ForeignKey(User, related_name = "posts")
	board = models.ForeignKey(Board, related_name = "posts")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
class Comment(models.Model):
	text = models.CharField(max_length=255)
	poster = models.ForeignKey(User, related_name = "comments")
	post = models.ForeignKey(Post, related_name = "comments")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
class Usercomment(models.Model):
	text = models.CharField(max_length=255)
	poster = models.ForeignKey(User, related_name = "usercomments")
	user = models.ForeignKey(User, related_name = "messages")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)