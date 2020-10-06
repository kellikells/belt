
from django import http
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import *
import bcrypt
from django.contrib import messages # flash messages
from .models import *

# ====================================================



# ====================================================
def index(request):
    request.session.clear()
    return render(request, 'belt_app/index.html')

# ------------------------------------------------------------------------
def logout(request):
    request.session.clear()
    return redirect('/')

# ------------------------------------------------------------------------
def register(request):
    if request.method == "POST":

        # getting errors from User Manager
        errors = User.objects.basic_validator(request.POST)

        # if there are errors: go back to signin.html and display errors
        if len(errors):
            context = {
                "errors": errors
            }
            return render(request, 'belt_app/index.html', context)

        # if email is already in the database
        if len(User.objects.filter(email = request.POST['email'])) > 0:
            context = {
                "errors" : request.POST['email'] + ' : email already exists'
            }
            return render(request, 'belt_app/index.html', context)

        # -----------------------------------------------------------------
        # NO ERRORS: ADD USER TO DATABASE
        else:

            # use bcrypt to hash password
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            # create User
            new_user = User(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password_hash=password_hash)

            new_user.save()

            return redirect('/register_success/')
           
# ------------------------------------------------------------------------
def register_success(request):
    context = {
        "messages": "you successfully registered"
    }
    return render(request, 'belt_app/index.html', context)

# ------------------------------------------------------------------------
def login(request):

 if request.method == "POST":
        errors = {}

        if len(request.POST['email']) < 1:
            errors['Enter your email'] = "Enter your email"
        if len(request.POST['password']) < 1:
            errors['Enter your password'] = "Enter your password"
        
        # if email is not in the database:
        if len(User.objects.filter(email = request.POST['email'])) < 1 :
            errors['Email does not exist, please register'] = "Email does not exist, please register"
        
        if len(errors):
            context = {
                "errors": errors
            }
            return render(request, 'belt_app/index.html', context)

        else: 
            # saving user object
            this_user = User.objects.get(email = request.POST['email'])

            # if password matches database password ************************
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password_hash.encode()):
                if 'user_id' not in request.session:
                    request.session['user_id'] = this_user.id
                
                if 'user_alias' not in request.session:
                    request.session['user_alias'] = this_user.alias
                return redirect('/login_success/')   

            # .............................................................
                
            # if password doens't match database password
            else: 
                errors['password doesn''t match'] = "password doesn''t match"
                context = {
                    "errors": errors
                }
                return render(request, 'belt_app/index.html', context)
# ------------------------------------------------------------------------
def login_success(request):
    context = {

        # getting reviews, newest first, limit 3
        "results": Review.objects.all().order_by("-updated_at")[:3],

        # getting all the books in database 
        "book_results": Book.objects.all().order_by("title")
    }
    

    return render(request, 'belt_app/books.html', context)

# ------------------------------------------------------------------------
def addReview(request, id):

    if request.method == "POST":

        # getting errors from Comment Manager
        errors = Review.objects.basic_validator(request.POST)

        # if there are errors: go back to signin.html and display errors
        if len(errors):
            context = {
                "errors": errors,

                # getting reviews, newest first, limit 3
                "results": Review.objects.all().order_by("-updated_at")[:3],

                # getting all the books in database 
                "book_results": Book.objects.all().order_by("title")
            }
            return render(request, 'belt_app/add.html', context)

        else:
            if request.POST['new-author']:

                # create new author 
                this_author = Author(name= request.POST['new-author'])
                this_author.save()

                # # create new book
                # this_book = Book(author_id = this_author, title = request.POST['title'])
                # this_book.save()
                
            
            else:

                # reference an existing author
                this_author = Author.objects.get(id= request.POST['old-author'])

                # this_book = Book(author_id = this_author, title = request.POST['title'])
            

            # create new book
            this_book = Book(author_id = this_author, title = request.POST['title'])
            this_book.save()

            # save user to var
            this_user = User.objects.get(id = id)

            # create review
            this_review = Review(book_id = this_book, user_id = this_user, content = request.POST['content'], rating = request.POST['rating'])
            
            this_review.save()

            return redirect('/addPage/')

# ------------------------------------------------------------------------
def addPage(request):
    context = {
        "author_results" : Author.objects.all()
    }
 
    return render(request, 'belt_app/add.html', context)

# ------------------------------------------------------------------------
def get_book_review(request, book_id):
    book = Book.objects.get(id = book_id)
    this_reviews = book.reviews.all().order_by("-updated_at")
    context = {
        "book": Book.objects.get(id = book_id),
        # "this_book_reviews": book.reviews().order_by("-updated_at"),
        "this_book_reviews": this_reviews,
        "image": "static/filled_star.jpg",
        "total": len(this_reviews),

        # star images for ratings
        "filled": "../../static/filled_star.jpg",
        "empty": "../../static/white_star.jpg"
    }
    return render(request, 'belt_app/bookreview.html', context)

# ------------------------------------------------------------------------
def booksPage(request):
    context = {

        # getting reviews, newest first, limit 3
        "results": Review.objects.all().order_by("-updated_at")[:3],

        # getting all the books in database 
        "book_results": Book.objects.all().order_by("title"),

        # star images for ratings
        "filled": "../../static/filled_star.jpg",
        "empty": "../../static/white_star.jpg"
    }
    return render(request, 'belt_app/books.html', context)

# ------------------------------------------------------------------------
def getUser(request, user_id):

    context = {
        "user_results": User.objects.get(id = user_id),
        "review_results": User.objects.get(id = user_id).user_reviews.all(),
        "count": User.objects.get(id = user_id).user_reviews.all().count()

    }

    return render(request, 'belt_app/users.html', context)

# ------------------------------------------------------------------------
def delete_review(request, book_id, review_id):
    if request.method == "POST":

        Review.objects.get(id=review_id).delete()

    return redirect('/login_success/')

# ------------------------------------------------------------------------
def additionalReview(request, book_id):
    if request.method == "POST":

        # getting errors from Comment Manager
        errors = Review.objects.basic_validator(request.POST)

        # if there are errors: go back to signin.html and display errors
        if len(errors):
            book = Book.objects.get(id = book_id)
            this_book_reviews = book.reviews().order_by("-updated_at")
            context = {
                "book": book,
                "this_book_reviews": this_book_reviews,
                "errors" : errors
            }
            image = "static/filled_star.jpg"
   
            return render(request, 'belt_app/bookreview.html', context, image=image, total=len(this_book_reviews))

        else:

            this_book = Book.objects.get(id = book_id)

            # save user to var
            this_user = User.objects.get(id = request.session['user_id'])

            # create review
            this_review = Review(book_id = this_book, user_id = this_user, content = request.POST['content'], rating = request.POST['rating'])
        
            this_review.save()

            return redirect('/get_book_review/' + book_id + '/')
        
# ------------------------------------------------------------------------



# ------------------------------------------------------------------------




# ------------------------------------------------------------------------
