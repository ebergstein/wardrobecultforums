from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib import messages
from .models import Post, Comment, Board, Usercomment
from ..logreg.models import User, Admin
from profanity import profanity 

# Create your views here.
def board(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	board = Board.objects.get(id = id)
	message = ""
	if not 'page' in request.session:
		request.session['page'] = 1
	request.session['page'] = int(request.session['page'])
	value = request.session['page'] * 10
	##if value > 10000:
		##value = 10
	posts = Post.objects.filter(board = board)
	if request.session['page'] == 1:
		posts = Post.objects.all().order_by('-created_at')[:10]
	else:
		posts = Post.objects.annotate(total = Count('id')).order_by('-created_at')[value - 10:value]
		message += "<a href = '{}'>Previous:</a> ".format(reverse("forum:previous"))
	if len(posts) >= 10:
		try:
			next = Post.objects.annotate(total = Count('id'))[value]
		except IndexError:
			pass
		else:
			message += "<a href = '{}'>Next:</a><br>".format(reverse("forum:next"))
	pages = ""
	all = Post.objects.all()
	num = len(all) / 10
	##print num
	if num > 1:
		pages += "<div class = 'pages'><p>Pages:</p>"
		for i in range(1, num + 2):
			if not i == request.session['page']:
				pages += "<a href = '{}'>{}</a> ".format(reverse("forum:page", kwargs={'id': i}), i)
		pages += "</div>"
	context = {
		"board": board,
		"posts": posts,
		"message": message,
		"pages": pages,
		"privilege": 0
	}
	try:
		user = User.objects.get(id = request.session['id'])
		admincheck = Admin.objects.get(users__id = request.session['id'])
		context['privilege'] = admincheck.privilege_level
		print "tried"
	except:
		pass
	return render(request, 'forums/index.html', context)
	
def index(request):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	boards = Board.objects.all().order_by('-created_at')
	context = {
		"boards": boards,
		"privilege": 0
	}
	try:
		user = User.objects.get(id = request.session['id'])
		admincheck = Admin.objects.get(users__id = request.session['id'])
		context['privilege'] = admincheck.privilege_level
		print "tried"
	except:
		pass
	return render(request, 'forums/boards.html', context)

def add(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	board = Board.objects.get(id = id)
	text = profanity.censor(request.POST['text'])
	user = User.objects.get(id = request.session['id'])
	Post.objects.create(text = text, poster = user, board = board)
	request.session['comment'] = 1
	return redirect(reverse('forum:board', kwargs={'id': id}))

def addboard(request):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	description = profanity.censor(request.POST['description'])
	header = request.POST['header']
	Board.objects.create(header = header, description = description)
	request.session['comment'] = 1
	return redirect(reverse('forum:index'))

def next(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['page'] += 1
	return redirect(reverse('forum:board', kwargs={'id': id}))

def previous(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['page'] -= 1
	return redirect(reverse('forum:board', kwargs={'id': id}))

def nextcomment(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] += 1
	return redirect(reverse('forum:post', kwargs={'id': id}))

def previouscomment(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] -= 1
	return redirect(reverse('forum:post', kwargs={'id': id}))
	
def nextusercomment(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] += 1
	return redirect(reverse('forum:user', kwargs={'id': id}))

def previoususercomment(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] -= 1
	return redirect(reverse('forum:user', kwargs={'id': id}))

def init(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] = 1
	return redirect(reverse('forum:post', kwargs={'id': id}))
	
def inituser(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] = 1
	return redirect(reverse('forum:user', kwargs={'id': id}))
	
def initboard(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['page'] = 1
	return redirect(reverse('forum:board', kwargs={'id': id}))

def page(request, id, page):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['page'] = page
	return redirect(reverse('forum:board', kwargs={'id': id}))

def commentpage(request, id, page):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] = page
	return redirect(reverse('forum:post', kwargs={'id': id}))
	
def usercommentpage(request, id, page):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['comment'] = page
	return redirect(reverse('forum:user', kwargs={'id': id}))

def post(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	post = Post.objects.get(id = id)
	board = post.board
	comments = Comment.objects.filter(post = post)
	message = ""
	pages = ""
	context = {}
	if not 'comment' in request.session:
		request.session['comment'] = 1
	request.session['comment'] = int(request.session['comment'])
	##if request.session['comment'] > 10000:
		##int(request.session['comment']) = 1
	if request.session['comment'] == 1:
		comments = Comment.objects.filter(post = post).order_by('created_at')[:9]
		if len(comments) >= 9:
			value = (request.session['page']) * 10
			try:
				next = Comment.objects.filter(post = post)[value - 1]
			except IndexError:
				pass
			else:
				print next.text
				message += "<a href = '{}'>Next:</a><br>".format(reverse("forum:nextcomment", kwargs={'id': id}))
		context = {
			"header": post,
			"post": post,
			"board": board,
			"comments": comments,
			"message": message,
			"privilege": 0
		}
	else:
		value = request.session['comment'] * 10
		header =  Comment.objects.filter(post = post).order_by('created_at')[value - 11]
		comments = Comment.objects.filter(post = post).order_by('created_at')[value - 10: value - 1]
		message += "<a href = '{}'>Previous:</a><br>".format(reverse("forum:previouscomment", kwargs={'id': id}))
		if len(comments) >= 9:
			value = (request.session['comment']) * 10
			try:
				next = Comment.objects.filter(post = post)[value-1]
			except IndexError:
				pass
			else:
				message += "<a href = '{}'>Next:</a><br>".format(reverse("forum:nextcomment", kwargs={'id': id}))
		context = {
			"header": header,
			"post": post,
			"board": board,
			"comments": comments,
			"message": message,
			"privilege": 0
		}
	request.session['comment'] = int(request.session['comment'])
	all = Comment.objects.filter(post = post)
	num = len(all) / 10
	##print num
	if num > 1:
		pages += "<div class = 'pages'><p>Pages:</p>"
		for i in range(1, num + 2):
			if not i == request.session['page']:
				pages += "<a href = '{}'>{}</a> ".format(reverse("forum:page", kwargs={'id': i}), i)
		pages += "</div>"
	context["pages"] = pages
	try:
		user = User.objects.get(id = request.session['id'])
		admincheck = Admin.objects.get(users__id = request.session['id'])
		context['privilege'] = admincheck.privilege_level
		print "tried"
	except:
		pass
	return render(request, 'forums/post.html', context)
	
def user(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	currentuser = User.objects.get(id = id)
	comments = Usercomment.objects.filter(user = currentuser)
	message = ""
	pages = ""
	context = {}
	if not 'comment' in request.session:
		request.session['comment'] = 1
	request.session['comment'] = int(request.session['comment'])
	##if request.session['comment'] > 10000:
		##int(request.session['comment']) = 1
	if request.session['comment'] == 1:
		comments = Usercomment.objects.filter(user = currentuser).order_by('created_at')[:9]
		if len(comments) >= 9:
			value = (request.session['page']) * 10
			try:
				next = Usercomment.objects.filter(user = currentuser)[value - 1]
			except IndexError:
				pass
			else:
				print next.text
				message += "<a href = '{}'>Next:</a><br>".format(reverse("forum:nextusercomment", kwargs={'id': id}))
		context = {
			"header": post,
			"user": currentuser,
			"id": request.session['id'],
			"comments": comments,
			"message": message,
			"privilege": 0
		}
	else:
		value = request.session['comment'] * 10
		header =  Usercomment.objects.filter(user = currentuser).order_by('created_at')[value - 11]
		comments = Usercomment.objects.filter(user = currentuser).order_by('created_at')[value - 10: value - 1]
		message += "<a href = '{}'>Previous:</a><br>".format(reverse("forum:previoususercomment", kwargs={'id': id}))
		if len(comments) >= 9:
			value = (request.session['comment']) * 10
			try:
				next = Usercomment.objects.filter(user = currentuser)[value-1]
			except IndexError:
				pass
			else:
				message += "<a href = '{}'>Next:</a><br>".format(reverse("forum:nextcomment", kwargs={'id': id}))
		context = {
			"header": header,
			"user": currentuser,
			"id": request.session['id'],
			"usercomments": comments,
			"message": message,
			"privilege": 0
		}
	request.session['comment'] = int(request.session['comment'])
	all = Usercomment.objects.filter(user = currentuser)
	num = len(all) / 10
	##print num
	if num > 1:
		pages += "<div class = 'pages'><p>Pages:</p>"
		for i in range(1, num + 2):
			if not i == request.session['page']:
				pages += "<a href = '{}'>{}</a> ".format(reverse("forum:page", kwargs={'id': i}), i)
		pages += "</div>"
	context["pages"] = pages
	try:
		user = User.objects.get(id = request.session['id'])
		admincheck = Admin.objects.get(users__id = request.session['id'])
		context['privilege'] = admincheck.privilege_level
		print "tried"
	except:
		pass
	try:
		admincheck = Admin.objects.get(users__id = id)
		context['userprivilege'] = admincheck.privilege_level
		print "tried"
	except:
		pass
	return render(request, 'forums/user.html', context)

def comment(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	post = Post.objects.get(id = id)
	text = profanity.censor(request.POST['text'])
	user = User.objects.get(id = request.session['id'])
	Comment.objects.create(text = text, poster = user, post = post)
	return redirect(reverse('forum:post', kwargs={'id': id}))
	
def usercomment(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	user = User.objects.get(id = id)
	text = profanity.censor(request.POST['text'])
	poster = User.objects.get(id = request.session['id'])
	Usercomment.objects.create(text = text, poster = poster, user = user)
	return redirect(reverse('forum:user', kwargs={'id': id}))

def back(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['page'] = 1
	return redirect(reverse('forum:board', kwargs={'id': id}))
	
def backboard(request):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	request.session['page'] = 1
	return redirect(reverse('forum:index'))

def delete(request, id, board):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	Post.objects.get(id = id).delete();
	request.session['page'] = 1
	return redirect(reverse('forum:board', kwargs={'id': board}))

def delcom(request, id, comment):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	Comment.objects.get(id = comment).delete();
	request.session['comment'] = 1
	return redirect(reverse('forum:post', kwargs={'id': id}))
	
def delusercom(request, id, comment):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	Usercomment.objects.get(id = comment).delete();
	request.session['comment'] = 1
	return redirect(reverse('forum:user', kwargs={'id': id}))

def logout(request):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	del request.session['first_name']
	del request.session['id']
	return redirect(reverse('login:home'))
	
def promote(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	user = User.objects.get(id = id)
	Admin.objects.create(users = user, privilege_level = 1)
	return redirect(reverse('forum:user', kwargs={'id': id}))
	
def admin(request):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	try:
		admincheck = Admin.objects.get(users__id = request.session['id'])
	except:
		return redirect(reverse('forum:index'))
	users = User.objects.all()
	context = {
		"users": users,
		"id": request.session['id'],
		"privilege": admincheck.privilege_level
	}
	return render(request, 'forums/admin.html', context)
	
def deleteuser(request, id):
	try:
		admin = Admin.objects.get(users_id = id)
		if admin.privilege_level < 2:
			admin.delete()
		else:
			return redirect(reverse('forum:admin'))
	except:
		pass
	User.objects.get(id = id).delete()
	return redirect(reverse('forum:admin'))
	
def description(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	user=User.objects.get(id = id)
	user.description = profanity.censor(request.POST['text'])
	user.save()
	return redirect(reverse('forum:user', kwargs={'id': id}))
	
def gender(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	user=User.objects.get(id = id)
	user.gender = profanity.censor(request.POST['text'])
	user.save()
	return redirect(reverse('forum:user', kwargs={'id': id}))
	
def location(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	user=User.objects.get(id = id)
	user.location = profanity.censor(request.POST['text'])
	user.save()
	return redirect(reverse('forum:user', kwargs={'id': id}))
	
def reset(request, id):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	old = request.POST['old']
	new = request.POST['new']
	confirm = request.POST['confirm']
	user=User.objects.get(id = id)
	check = User.objects.passvalidator(id, old, new, confirm)
	if check['errors'] == []:
		prehash = User.objects.bcryptor(request.POST['new'])
		pwhash = prehash['pwhash']
		user.pwhash = pwhash
		user.save()
		messages.add_message(request, messages.ERROR, "Password Changed.")
	else:
		for errors in check['errors']:
			messages.add_message(request, messages.ERROR, errors)
	return redirect(reverse('forum:user', kwargs={'id': id}))
	
def close(request, id):
	try:
		admin = Admin.objects.get(users_id = id).delete()
	except:
		pass
	User.objects.get(id = id).delete()
	del request.session['first_name']
	del request.session['id']
	return redirect(reverse('login:home'))