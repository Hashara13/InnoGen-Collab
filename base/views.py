from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm



def home(request):
    
    #fetch all queys in Room model to view
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'base/home.html',context)

def room(request, room_id):
    room = Room.objects.get(id=room_id)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def add_room(request):
    
    # fetch ModelForm
    form=RoomForm()
    context = {'form':form}
    return render(request, 'base/collab_form.html', context)

