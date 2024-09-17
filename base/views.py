from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def signinPage(request):
    page='signin'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        username=request.POST.get('username')
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
    return redirect('home')

def signUpPage(request):
    page='signup'
    return render(request,'base/signin_up.html')

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
    
    #fetch all queys in Room model to view
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'r_count':r_count}
    return render(request,'base/home.html',context)

def room(request, room_id):
    room = Room.objects.get(id=room_id)
    context = {'room': room}
    return render(request, 'base/room.html', context)

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