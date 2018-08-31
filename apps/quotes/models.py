from __future__ import unicode_literals

from django.db import models
import re
import datetime
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
# Create your models here.
class UserManager(models.Manager):
	def login_validator(self,postData):
		
		errors = {}
		#email field
		if len(postData['email']) < 1:
			errors['email_error'] = "Email field is required"
		elif not re.compile(r'^[a-zA-Z0-9+-_]+@[a-zA-Z0-9+-_]+.[a-zA-Z0-9+-_]$').match(postData["email"]):
			errors['email_error'] = "Enter an valid email id"
		

		#Password Field
		if len(postData['password']) < 1:
			errors['password_error'] = "Password field is required"
		elif len(postData['password']) < 8:
			errors['password_error'] = "Password cannot be less than 8 characters"
		elif bcrypt.checkpw(postData['password'].encode(),User.objects.get(email=postData['email']).password.encode()) == False:
			errors["password_error"] = "check your password again"
		return errors
		
		print "*****end of login_validator*******"
	
	def register_validator(self,postData):
		errors = {}
		#Name Field

		if len(postData['name']) < 1:
			errors['name_error'] = "Name field cannot be blank"
		elif len(postData['name']) < 2:
			errors['name_error'] = "Name field has to be more than 2 characters"
		elif not re.compile(r'^[a-zA-Z]{2,}$').match(postData['name']):
			errors['name_error'] = "Name field should be non-numeric"

		#Alias field
		if len(postData['alias']) < 1:
			errors['alias_error'] = "Alias field cannot be blank"
		elif len(postData['alias']) < 2:
			errors['alias_error'] = "Alias field has to be more than 2 characters"
		elif not re.compile(r'^[a-zA-Z]+$').match(postData['alias']):
			errors['alias_error'] = "Alias field should be non-numeric"

		#Email Field
		if len(postData['email']) < 1:
			errors['email_error'] = "Email field is required"
		elif len(User.objects.filter(email=postData['email'])) > 0:
			errors['email_error'] = "Duplicate email"
		elif not re.compile(r'^[a-zA-Z0-9+-_]+@[a-zA-Z0-9+-_]+.[a-zA-Z0-9+-_]$').match(postData["email"]):
			errors['email_error'] = "Enter an valid email id"


		#Password Field
		if len(postData['password']) < 1:
			errors['password_error'] = "Password field is required"
		elif len(postData['password']) < 8:
			errors['password_error'] = "Password cannot be less than 8 characters"
		#confirm password
		elif not postData['password'] == postData['confirm_pwd']:
			errors['password_error'] = "Password and confirm password are not matching"
		#birthday field
		if postData['bday'] == None:
			errors['bday'] = "Birthday field cannot be blank"

		return errors

class QuoteManager(models.Manager):
	
	def quote_validator(self,postData):

		errors = {}

		if len(postData['quote_author']) < 3:
			errors['quote_author_error'] = "Quotes author field cannot be less than 3char"
		elif len(postData['quote_author']) < 0:
			errors['quote_author_error'] = "Quotes cannot be empty"
		if len(postData['message']) < 3:
			errors['message_error'] = "Quotes cannot be less than 10 characters"
		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField(max_length=254)
	password = models.CharField(max_length=255)
	bday = models.DateField(default=datetime.date.today)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	
	def __unicode__(self):
		return "id : " + str(self.id) + ", name : " + self.name + \
				", email : " + self.email + ", password : " + self.password +\
				" , birthday : " + str(self.bday)

	objects = UserManager()


class Quote(models.Model):
	author = models.CharField(max_length=255)
	content = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	uploader = models.ForeignKey(User, related_name="uploaded_quotes")
	liked_users = models.ManyToManyField(User, related_name="liked_quotes")


	def __unicode__(self):
		return "id : " + str(self.id) + ", author : " + self.author + \
		", content : " + str(self.content) + " , uploader : " + str(self.uploader) + \
		" , liked_users : " + str(self.liked_users)

	objects = QuoteManager()
 



