from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Admin

def index(request):
    return render(request, 'logreg/index.html')

def register(request):
    user = User.objects.regvalidator(request.POST['first'], request.POST['last'], request.POST['email'], request.POST['password'], request.POST['confirm'])
    if user['errors'] != []:
        for errors in user['errors']:
            messages.add_message(request, messages.ERROR, errors)
        return redirect(reverse('login:home'))
    prehash = User.objects.bcryptor(request.POST['password'])
    pwhash = prehash['pwhash']
    User.objects.create(first_name = request.POST['first'], last_name = request.POST['last'], email = request.POST['email'], 
    pwhash = pwhash, description = "", gender = "", location = "", title = "")
    request.session['first_name'] = request.POST['first']
    check = User.objects.get(email = request.POST['email'])
    try:
    	Admin.objects.get(privilege_level = 2)
    except:
    	Admin.objects.create(users = check, privilege_level = 2)
    request.session['id'] = check.id
    request.session['first_name'] = check.first_name 
    return redirect(reverse('forum:index'))

def login(request):
    user = User.objects.logvalidator(request.POST['email'], request.POST['password'])
    if user['errors'] != []:
        for errors in user['errors']:
            messages.add_message(request, messages.ERROR, errors)
        return redirect(reverse('login:home'))
    namer = User.objects.get(email = request.POST['email'])
    request.session['id'] = namer.id
    request.session['first_name'] = namer.first_name
    return redirect(reverse('forum:index'))
    
def auto(request, first, last, email, password):
	try:
		User.objects.get(email = email)
	except:
		user = User.objects.regvalidator(first, last, email, password, password)
		if user['errors'] != []:
			for errors in user['errors']:
				messages.add_message(request, messages.ERROR, errors)
			return redirect(reverse('login:home'))
		prehash = User.objects.bcryptor(password)
		pwhash = prehash['pwhash']
		User.objects.create(first_name = first, last_name = last, email = email, pwhash = pwhash, description = "", 
		gender = "", location = "", title = "")
		request.session['first_name'] = first
		check = User.objects.get(email = email)
    	try:
    		Admin.objects.get(privilege_level = 2)
    	except:
    		Admin.objects.create(users = check, privilege_level = 2)
		request.session['id'] = check.id
		request.session['first_name'] = check.first_name 
		return redirect(reverse('forum:index'))
	user = User.objects.logvalidator(email, password)
	if user['errors'] != []:
		for errors in user['errors']:
			messages.add_message(request, messages.ERROR, errors)
		return redirect(reverse('login:home'))
	user = User.objects.logvalidator(email, password)
	namer = User.objects.get(email = email)
	request.session['id'] = namer.id
	request.session['first_name'] = namer.first_name
	return redirect(reverse('forum:index'))