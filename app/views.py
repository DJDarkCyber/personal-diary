from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from . models import Quotes, Diary
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def main(request):
	# htmlVars = {
	# 				"user": request.user.username,
	# 				"firstname": request.user.first_name,
	# 				"is_auth": request.user.is_authenticated
	# 			}
	if(request.user.is_authenticated == False):
		htmlVars = {
					"user": request.user.username,
					"firstname": "Anon",
					"is_auth": request.user.is_authenticated
				}
	else:
		htmlVars = {
					"user": request.user.username,
					"firstname": request.user.first_name,
					"is_auth": request.user.is_authenticated
				}
	return render(request, 'index.html', htmlVars)

def singIn(request):
	if(request.user.is_authenticated == False):
		htmlVars = {
					"user": request.user.username,
					"firstname": "Anon",
					"is_auth": request.user.is_authenticated
				}
	else:
		htmlVars = {
					"user": request.user.username,
					"firstname": request.user.first_name,
					"lastname": request.user.last_name,
					"is_auth": request.user.is_authenticated
				}
		return render(request, 'userSettings.html', htmlVars)
	return render(request, "signIn.html", htmlVars)

def registerForm(request):
	if(request.user.is_authenticated == False):
		htmlVars = {
					"user": request.user.username,
					"firstname": "Anon",
					"is_auth": request.user.is_authenticated
				}
	else:
		htmlVars = {
					"user": request.user.username,
					"firstname": request.user.first_name,
					"lastname": request.user.last_name,
					"is_auth": request.user.is_authenticated
				}
		return render(request, 'userSettings.html', htmlVars)
	return render(request, 'register.html', htmlVars)

def handleRegister(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		print(form.errors)
		if form.is_valid():
			print("VALID")
			username = form.cleaned_data.get("username")
			email = form.data.get("email")
			password = form.data.get("password1")
			firstName = form.data.get('first_name')
			lastName = form.data.get('last_name')
			print(password)
			User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
			user= User.objects.get(username=username)
			user.save()
			print(user.username)
			print(user.email)
			print(user.password)
			return redirect('SignIn')
		else:
			for field in form:
				for error in field.errors:
					messages.error(request, error)
			return redirect('Register')
	else:
		form = UserCreationForm()
	print("NOt VALID")
	return render(request, 'register.html')

def handleLogin(request):
	htmlVars = {
		"is_found": 1
	}
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			print("Valid")
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("index")
				
	else:
		form = AuthenticationForm()
	print(form.error_messages)
	print("In Valid")
	htmlVars = {
		"user": request.user.username,
		"firstname": "Anon",
		"is_auth": request.user.is_authenticated,
		"is_found": 0
	}
	for field in form:
		for error in field.errors:
			messages.error(request, error)
	# return redirect("SignIn")
	return render(request, 'signIn.html', htmlVars )

def userSettings(request):
	if request.user.is_authenticated:
		htmlVars = {
			"user": request.user.username,
			"firstname": request.user.first_name,
			"lastname": request.user.last_name,
			"is_auth": request.user.is_authenticated
		}
	else:

		
		htmlVars = {
			"user": request.user.username,
			"firstname": "Anon",
			"lastname": "",
			"is_auth": request.user.is_authenticated
		}
		return render(request, "signIn.html", htmlVars)
	return render(request, 'userSettings.html', htmlVars)


def handleLogout(request):
	logout(request)
	return redirect('index')

def changePassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		print(form.is_valid())
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			return redirect('index')
		else:
			for field in form:
				for error in field.errors:
					messages.error(request, error)
			return redirect("settings")
			# print(form.errors)

	else:
		
		form = PasswordChangeForm(request.user)	
	return render(request, 'userSettings.html')

def publicQuotes(request):
	
	quotes = Quotes.objects.all().order_by('-quotedAt')

	usrNames = []
	titles = []
	allQuotes = []
	quotedTimes = []
	for quote in quotes:
		usrNames.append(quote.usrName)
		titles.append(quote.title)
		allQuotes.append(quote.quote)
		quotedTimes.append(quote.quotedAt)
	items = zip(usrNames, quotedTimes, titles, allQuotes)
	paginator = Paginator(list(items), 20)
	page = request.GET.get("page")
	items = paginator.get_page(page)
	if request.user.is_authenticated:
		htmlVars = {
						"user": request.user.username,
						"is_auth": request.user.is_authenticated,
						"firstname": request.user.first_name,
						"items": items
					}
	else:
		htmlVars = {
						"user": request.user.username,
						"is_auth": request.user.is_authenticated,
						"firstname": "Anon",
						"items": items
					}
	return render(request, "quotes.html", htmlVars)


def handle_quote(request):
	if request.method == 'POST':
		auth_name = request.POST.get('auth_name')
		title = request.POST.get('quote_title')
		quote = request.POST.get('quote')
		q = Quotes(usrName=auth_name, title=title, quote=quote)
		q.save()
		return redirect('quotes')
	else:
		return render(request, 'quotes.html')

def handle_names(request):
	if request.method == 'POST':
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")

		user = request.user

		user.first_name = first_name
		user.last_name = last_name
		user.save()

		return redirect("index")
	else:
		return render(request, "userSettings.html")


def yourDiary(request):
	diaryCont = Diary.objects.filter(username=request.user.username).order_by("-addedAt")
	addAtTimes = []
	titles = []
	diary_contents = []

	for cont in diaryCont:
		addAtTimes.append(cont.addedAt)
		titles.append(cont.title)
		diary_contents.append(cont.diary_content)

	items = zip(addAtTimes, titles, diary_contents)
	paginator = Paginator(list(items), 10)
	page = request.GET.get("page")
	items = paginator.get_page(page)
	if request.user.is_authenticated:
		htmlVars = {
						"user": request.user.username,
						"is_auth": request.user.is_authenticated,
						"firstname": request.user.first_name,
						"items": items
					}
	else:
		
		htmlVars = {
						"user": request.user.username,
						"is_auth": request.user.is_authenticated,
						"firstname": "Anon",
						"items": items
					}
		return render(request, 'signIn.html', htmlVars)

	return render(request, 'diary.html', htmlVars)

def handle_diary(request):
	if request.method == "POST":
		username = request.user.username
		title = request.POST.get('diary_title')
		diary = request.POST.get('diary')
		q = Diary(username=username, title=title, diary_content=diary)
		q.save()
		return redirect('diary')
	else:
		return render(request, 'diary.html')


def aboutMe(request):
	if request.user.is_authenticated:
		htmlVars = {
						"user": request.user.username,
						"is_auth": request.user.is_authenticated,
						"firstname": request.user.first_name,
					}
	else:
		
		htmlVars = {
						"user": request.user.username,
						"is_auth": request.user.is_authenticated,
						"firstname": "Anon",
					}
	return render(request, 'about.html', htmlVars)