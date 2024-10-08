from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room,Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def signinPage(request):
    page='signin'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user dosen't have access")
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password  dosen't exist, try again")
    context={'page':page}
    return render(request,'base/signin_up.html',context)

def signOutPage(request):
    logout(request)
    context={'page':page}
    return redirect('home')

def signUpPage(request):
    # page='signup'
    form=UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred')
    return render(request,'base/signin_up.html',{'form':form})

def home(request):
    
    # search by Topics attr
    query=request.GET.get('query') if request.GET.get('query') !=None else ''
    
    rooms=Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(desc__icontains=query)
        )
    r_count=rooms.count()

    topics=Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__name__icontains=query))
    #fetch all queys in Room model to view
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'r_count':r_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)


def room(request, room_id):
    room = Room.objects.get(id=room_id)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        if request.user not in room.participants.all():
            room.participants.add(request.user)
        return redirect('room', room_id=room.id) 

    context = {
        'room': room,
        'room_messages': room_messages,
        'request': request,
        'participants':participants
    }
    return render(request, 'base/room.html', context)


def profilePage(request,room_id):
    user = User.objects.get(id=room_id)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request, 'base/profile_page.html', context)


@login_required(login_url='signin')
def add_room(request):
    
    # fetch ModelForm
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    context = {'form':form}
    return render(request, 'base/collab_form.html', context)


@login_required(login_url='signin')
def edit_room(request, room_id):
    room = Room.objects.get(id=room_id)
    # show existance values
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Unauthorized Access')
    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/collab_form.html', context)

@login_required(login_url='signin')
def remove_room(request, room_id):
    room = Room.objects.get(id=room_id)
    # # show existance values
    # form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Unauthorized Access')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    # context = {'form': form}
    return render(request, 'base/remove.html', {'obj':room})

@login_required(login_url='signin')
def remove_message(request, room_id):
    message = Message.objects.get(id=room_id)
    if request.user != message.user:
        return HttpResponse('Unauthorized Access')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/remove.html', {'obj':message})