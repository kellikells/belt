from __future__ import unicode_literals
from django.db import models
from django import forms
# for regular expressions 
import re 
# for validating an Email 
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# ---------------------------------------------

# MANAGER FOR VALIDATION
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 : 
            errors['name'] = "Enter a name"
        if len(postData['alias']) < 2:
            errors['alias'] = "Enter an alias"
        if not (postData['name']).isalpha() or not (postData['alias']).isalpha():
            errors['Name only include letters'] = "Name only include letters"
        
        if not (re.search(regex,postData['email'])):  
            errors['Invalid email'] = "Invalid email address"
        if len(postData['email']) < 1:
            errors['Add your email'] = "Add your email"
        if len(postData['password']) < 8:
            errors['Password must be at least 8 characters'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['Passwords don''t match'] = "Password don''t match"
        return errors
# ---------------------------------------------
class ReviewManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = "review content cannot be empty"
        if len(postData['rating']) > 1:
            errors['rating'] = "select a rating for your review"
        
        return errors

# ---------------------------------------------

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
    
    def __str__(self):
        return ('name = ' + self.name + ', alias = ' + self.alias + ', email = ' + self.email )

# ---------------------------------------------
class Author(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return ('author = ' + self.name)

# ---------------------------------------------
class Book(models.Model):
    # one-to-many relationship: one author to many books
    author_id = models.ForeignKey(Author, on_delete= models.CASCADE, related_name ="books")

    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return ('author_id = ' + str(self.author_id) + ', title = ' + self.title)

# ---------------------------------------------
class Review(models.Model):
    # one-to-many relationship: one book to many reviews
    book_id = models.ForeignKey(Book, on_delete= models.CASCADE, related_name = "reviews")

    #one-to-many relationship: one user to many reviews
    user_id = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "user_reviews")

    content = models.TextField()
    rating = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = ReviewManager()

    def __str__(self):
        return ('content = ' + self.content + ', rating = ' + str(self.rating))




# ---------------------------------------------


# ---------------------------------------------


# ---------------------------------------------


# ---------------------------------------------