from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .scrape import SubredditScraper
from .models import Scrape
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import Filter_Age
# Create your views here.


def check_age(age):
	if age.isnumeric() and age != "":
		return True
	else:
		return False
def check_feet(feet):
	if feet.isnumeric() and feet !="":
		return True
	else:
		return False
def check_inches(inches):
	if inches.isnumeric() and inches !="":
		return True
	else:
		return False

def check_h (feet, inches):
	if check_feet(feet) and check_inches(inches):
		return True
	else:
		return False


def homepage(request):
	bothflag = False
	ageflag = False
	heightflag = False
	age_f = Filter_Age() 
	if request.method == "POST":
		form = Filter_Age(request.POST)
		if form.is_valid():
				age = form.cleaned_data.get('age_f')
				feet = form.cleaned_data.get('h_feet')
				inches = form.cleaned_data.get('h_inches')
				height = str(feet)+"'"+str(inches)
				if check_age(age) and check_h(feet, inches):
					bothflag = True
				else:
					if check_age(age):
						ageflag = True
					if check_h(feet,inches):
						heightflag = True
				if ageflag:
					messages.success (request, f"Filtering for  {age} y/o")
					entry_list = Scrape.objects.filter(Scrape_age__exact = age).order_by('-Scrape_date')
					page = request.GET.get('page', 1)
					paginator = Paginator (entry_list, 15)
					try:
						entries = paginator.page(page)
					except PageNotAnInteger:
						entries = paginator.page(1)
					except EmptyPage:
						entries = paginator.page(paginator.num_pages)
					return render(request = request,
								  template_name='main/home.html',
								  context = {"scrape": Scrape.objects.all,
								  			"Entries": entries,
								  			"age_f": age_f})
				if heightflag:
					messages.success (request, f"Filtering for {height}")
					entry_list = Scrape.objects.filter(Scrape_height__exact = height).order_by('-Scrape_date')
					page = request.GET.get('page', 1)
					paginator = Paginator (entry_list, 15)
					try:
						entries = paginator.page(page)
					except PageNotAnInteger:
						entries = paginator.page(1)
					except EmptyPage:
						entries = paginator.page(paginator.num_pages)
					return render(request = request,
								  template_name='main/home.html',
								  context = {"scrape": Scrape.objects.all,
								  			"Entries": entries,
								  			"age_f": age_f})
				if bothflag:
					messages.success (request, f"Filtering for {age} y/o who are {height}")
					entry_list = Scrape.objects.filter(Scrape_height__exact = height).filter(Scrape_age__exact = age).order_by('-Scrape_date')
					page = request.GET.get('page', 1)
					paginator = Paginator (entry_list, 15)
					try:
						entries = paginator.page(page)
					except PageNotAnInteger:
						entries = paginator.page(1)
					except EmptyPage:
						entries = paginator.page(paginator.num_pages)
					return render(request = request,
								  template_name='main/home.html',
								  context = {"scrape": Scrape.objects.all,
								  			"Entries": entries,
								  			"age_f": age_f})
				else:
					if age!="" or height!="":
							messages.error(request, f"bruh you need to punch in numbers >_>")
					entry_list = Scrape.objects.all().order_by('-Scrape_date')
					page = request.GET.get('page', 1)
					paginator = Paginator (entry_list, 15)
					try:
						entries = paginator.page(page)
					except PageNotAnInteger:
						entries = paginator.page(1)
					except EmptyPage:
						entries = paginator.page(paginator.num_pages)
					return render(request = request,
								  template_name='main/home.html',
								  context = {"scrape": Scrape.objects.all,
								  			"Entries": entries,
								  			"age_f": age_f})
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages}")
	else:
		
		entry_list = Scrape.objects.all().order_by('-Scrape_date')
		page = request.GET.get('page', 1)
		paginator = Paginator (entry_list, 15)
		try:
			entries = paginator.page(page)
		except PageNotAnInteger:
			entries = paginator.page(1)
		except EmptyPage:
			entries = paginator.page(paginator.num_pages)
		return render(request = request,
					  template_name='main/home.html',
					  context = {"scrape": Scrape.objects.all,
					  			"Entries": entries,
					  			"age_f": age_f})

def update (request):
	response = redirect('/')
	f_count = 0
	s = SubredditScraper
	tup=s("brogress", sort = "new", lim = 100, age_ = "", gender_="", height_="").scraper()
	for elements in tup: #make not reversed for initial load
		f_lag = False
		removef_lag = False
		post_ = Scrape()
		for els in Scrape.objects.all():
			if els.Scrape_pid == elements[4]:
				f_lag = True
				f_count +=1
				break
		if f_lag == False:
			post_.Scrape_gender = elements[0]
			post_.Scrape_age = elements[1]
			post_.Scrape_weight =elements[3]	
			post_.Scrape_height =elements[2]
			post_.Scrape_pid = elements[4]
			post_.Scrape_url = elements [5]
			post_.Scrape_date = elements[6]
			post_.Scrape_len = elements[7]
			post_.Scrape_coms = elements[8]
			post_.Scrape_abstime = elements[9]
			post_.save()
	print ("Total of ", len(tup), " : ", f_count, " did not get added")
	return response

def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				messages.success (request, f"New Account Created: {username}")
				login (request, user)
				messages.success (request, f"You are logged in as: {username}")
				return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages}")
			return render(request, 
						"main/register.html",
						context={"form":form})

	form = UserCreationForm
	return render(request, 
				"main/register.html",
				context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully")
	return redirect("main:homepage")

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data =request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				messages.success (request, f"You are logged in as: {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password")
		else:
				messages.error(request, "Invalid username or password")

	form = AuthenticationForm()
	return render(request,
				"main/login.html",
				{"form":form})
