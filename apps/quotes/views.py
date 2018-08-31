from django.shortcuts import render, redirect

from models import User, Quote
import bcrypt
from django.contrib import messages
from django.contrib.auth import logout


def index(request):

	return render(request, "belt/index.html")

def logval(request):
	
	errors = User.objects.login_validator(request.POST)
	print "inside logval"
	if len(errors):
		for key,value in errors.iteritems():
			messages.error(request,value,extra_tags=key)
		return redirect('/')
	else:
		email = request.POST['email']
		if "email" not in request.session:
			request.session['email'] = email
	return redirect("/quotes")

def regval(request):
	
	errors = User.objects.register_validator(request.POST)

	if len(errors):
		for key,value in errors.iteritems():
			messages.error(request,value,extra_tags=key)
		return redirect('/')
	else:
		hash_pwd = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
		User.objects.create(
							name=request.POST['name'],
							alias=request.POST['alias'],
							email=request.POST['email'],
							password=hash_pwd)

		if "email" not in request.session:
			request.session['email'] = request.POST['email']
		if "id" not in request.session:
			request.session['id'] = User.objects.get(email=request.POST['email']).id
		
		return redirect("/quotes")

def show_quotes(request):

	if "login" not in request.session:
		request.session['login'] = True

	context = {
		"users" : User.objects.all(),
	 	"welcome_user" : User.objects.get(email=request.session['email']),
	 	"all_quotes" : Quote.objects.all().exclude(liked_users=User.objects.get(email=request.session['email'])),
	 	"fav_quotes" : User.objects.get(email=request.session['email']).liked_quotes.all(),
    }

	return render(request, "belt/quotes.html", context)

def allquote_add(request):
	
	errors = Quote.objects.quote_validator(request.POST)

	if errors:
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/quotes')
	else:
		if request.method == "POST":
	
			user = User.objects.get(email=request.session['email'])
			
			Quote.objects.create(author=request.POST['quote_author'],\
				content=request.POST['message'],uploader=user)

	return redirect('/quotes')

def addfq(request, id):
		
	user = User.objects.get(email=request.session['email'])
	quote = Quote.objects.get(id=id)

	quote.liked_users.add(user)

	return redirect('/quotes')


def removefq(request, id):
	
	

	user = User.objects.get(email=request.session['email'])
	quote = Quote.objects.get(id=id)

	quote.liked_users.remove(user)

	return redirect('/quotes')

def show_user(request,id):

	u = User.objects.get(id=id)

	context = {
				"users" : User.objects.get(id=id),
				"count" : User.objects.get(id=id).uploaded_quotes.count(),
				"quotes" : User.objects.get(id=id).uploaded_quotes.all(),
			}
	return render(request, "belt/show_user.html",context)
def logoutpage(request):
	
	logout(request)
	return redirect('/')







