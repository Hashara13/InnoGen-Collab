from django.shortcuts import render
from django.http import HttpResponse
from .models import Room



def home(request):
    
    #fetch all queys in Room model to view
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'base/home.html',context)

def room(request):
   #fetch one queys in Room model to view based on single id
    rooms=Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'/base/room.html',context)
