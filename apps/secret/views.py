from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Secret
from django.db.models import Count
import bcrypt


#New User Registration Logic
def register(request):

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    data = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "password": password,
    "confirm_password": confirm_password
    }
    user = User.objects.register(data)

    if user:
        for i in range(0,len(user)):
            messages.error(request, user[i])
            return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        create = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
        current_user = User.objects.get(first_name=request.POST['first_name'])
        request.session['id'] = current_user.id
        return redirect('/secrets')

#Returning user login
def login(request):
    email = request.POST['email']
    password = request.POST['password'].encode()
    data = {"email": email, "password": password}

    user = User.objects.login(data)
    if user:
        for i in range(0,len(user)):
            messages.error(request, user[i])
            return redirect('/')

    else:
        current_user = User.objects.get(email=email)
        print current_user.first_name
        print current_user.id

        request.session['id'] = current_user.id
        return redirect('/secrets')


# Create your views here.
def index(request):
    return render(request, 'secret/index.html')

def secrets(request):
    user_like = []
    current_user = User.objects.get(id=request.session['id'])
    secrets = Secret.objects.all().order_by('-created_at')
    for secret in secrets:
        secret.like.all()
        for like in secret.like.all():
            if like.id == request.session['id']:
                user_like.append(secret.id)
    context = {
    "secrets":secrets[:5],
    "current_user": current_user,
    "user_like": user_like,
    }
    return render(request, 'secret/secrets.html', context)

def most_popular(request):
    user_like = []
    secrets = Secret.objects.all().annotate(likeNum = Count('like')).order_by('-likeNum')
    for secret in secrets:
        secret.like.all()
        for like in secret.like.all():
            if like.id == request.session['id']:
                user_like.append(secret.id)
    context = {
    "secrets":secrets,
    "user_like": user_like,
    }
    return render(request, 'secret/most_popular.html', context)

def add_secret(request):
    thisuser = User.objects.get(id=request.session['id'])
    Secret.objects.create(content=request.POST['secret_content'], user=thisuser)
    return redirect('/secrets')

def like(request, id):
    thisuser = User.objects.get(id=request.session['id'])
    secret = Secret.objects.get(id=id)
    secret.like.add(thisuser)
    return redirect('/secrets')

def delete(request, id):
    Secret.objects.filter(id=id).delete()
    return redirect('/secrets')

def logout(request):
    request.session['id'] = ''
    return redirect('/')
