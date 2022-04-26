from django.shortcuts import render, redirect
from django.contrib import messages
from matplotlib import type1font
from .models import User, Post
import bcrypt
import requests
import urllib
import os


def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password').encode("utf8")
        confirmPass = request.POST.get('confirmPass').encode("utf8")
        inputs = [email, username, password, confirmPass]

        # checking if confirm password matches password   
        if (password != confirmPass):
            messages.error(request, "The passwords do not match.")
            return redirect('signup')

        for inp in inputs:
            if inp == '':
                messages.error(request, "Please fill all the boxes.")
                return redirect('signup')

        if password != '' and len(password) < 6:
            messages.error(request, "Your password must be at least 6 charecters.")
            return redirect('signup')
        

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists. If this is you, please log in.")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "An account with this username already exists. Please pick another one.")
            return redirect('signup')

        else:
            salt = bcrypt.gensalt()
            user = User()
            user.email = email
            user.username = username
            user.password = bcrypt.hashpw(password, salt)
            user.salt = salt
            user.save()
            return redirect('login')

    return render(request, 'later/signup.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password').encode("utf8")
        inputs = [email, password]

        print (type(email))

        for inp in inputs:
            if inp == '':
                messages.error(request, "Please fill all the boxes.")
                return redirect('login')

        if "@" not in email:
            messages.error(request, "Please enter your email address.")
            return redirect('login')

        if User.objects.filter(email=email).exists():
            saved_hashed_pass = User.objects.filter(email=email).get().password.encode("utf8")[2:-1]
            saved_salt = User.objects.filter(email=email).get().salt.encode("utf8")[2:-1]
            user  = User.objects.filter(email=email).get()
            request.session["username"] = user.username

           
            salted_password = bcrypt.hashpw(password, saved_salt)
            if salted_password == saved_hashed_pass:
                return redirect('dashboard')
            else:
                messages.error(request, "Your password is incorrect.")
                return redirect('login')

        else:
            messages.error(request, "An account with this email does not exist. Please sign up.")
            return redirect('login')

    return render(request, 'later/index.html')


#def add_to_reading_list(request):


    # want stay in booksearch but not working
    return render(request, 'later/dashboard.html')


def logout(request):
    del request.session["username"]

    return redirect('login')


def dashboard(request):

    user = User.objects.get(username=request.session["username"])

    context = {
        "reading_list" : [{   
                "img": f"http://books.google.com/books/content?id={book_id}&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                "link": f"api/book/{book_id}",
                "name": f"{user.reading_list[book_id]['book_name']}",
                "id": book_id,
            }
            for book_id in user.reading_list.keys()     
        ], 
        "finished" : [{   
                "img": f"http://books.google.com/books/content?id={book_id}&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                "link": f"api/book/{book_id}",
                "name": f"{user.finished[book_id]['book_name']}",
                "id": book_id,
            }
            for book_id in user.finished.keys()     
        ], 
        
    }



    ##, "finished": user.finished
    

    return render(request, 'later/dashboard.html', {"context": context})




def back(req):
    a = req.META


def apiCall(req):
    if req.method == "GET":
        bookNameToBeSearched = req.GET.get('bookName')

    # env_api_key = os.environ.get('GOOGLE_BOOKS_API_KEY')
    # print("gb api key: %s" % env_api_key)
    api_key = "AIzaSyDzp_LKa5V2u5vtPu1cMtTKM287r7KW50s"

    google_host = "https://www.googleapis.com/books/v1/volumes"

    f = {'q': bookNameToBeSearched, 'key': api_key}
    google_host += "?" + urllib.parse.urlencode(f)
    res = requests.get(google_host)



    req.session["data"] = res.json()

    return render(req, "later/bookSearch.html", {'api_res': res.json()})


#def bookSearch(request):
    return render(request, "later/bookSearch.html", {'api_res': request.session['data']})

def home(req):
         return redirect('dashboard')



def book(req, id):
    

    api_key = "AIzaSyDzp_LKa5V2u5vtPu1cMtTKM287r7KW50s"

    google_host = "https://www.googleapis.com/books/v1/volumes/" + id

    f = {'key': api_key}
    google_host += "?" + urllib.parse.urlencode(f)
    res = requests.get(google_host)

    req.session["data"] = res.json()



    context = {
        "book_looked_up": res.json(),
        "opinions" :Post.objects.all()
            
    }

    

    return render(req, 'later/book.html', context)

def addToReadingList(req):
    username = req.session.get("username")
    user = User.objects.get(username=username)
    book_id = req.POST.get("bookToAdd")
    user.reading_list[req.POST.get("bookToAdd")] = {"book_name": req.POST.get("bookname"), "img": f"http://books.google.com/books/content?id={book_id}&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api", "id": book_id }
    user.save()
    return redirect('dashboard')

def removeFromReadingList(req):
    username = req.session.get("username")
    user = User.objects.get(username=username)
    bookData = user.reading_list[req.POST.get("bookid")]
    del user.reading_list[req.POST.get("bookid")]
    user.finished[bookData["id"]] = bookData
    user.save()
    return redirect('dashboard')


def comments(req):
    comment = Post()
    book_id = req.POST.get("bookToComment")
    username = req.session.get("username")
    user = User.objects.get(username=username)
    message = req.POST.get("message")
    comment.book_id = book_id
    comment.user = user
    comment.message = message
    comment.save()
    return redirect(f"api/book/{book_id}")
