from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm



def home(request):
    query=request.GET.get('query') if request.GET.get('query') !=None else ''
    
    rooms=Room.objects.filter(topic__name__icontains=query)
    topics=Topic.objects.all()
    
    #fetch all queys in Room model to view
    rooms=Room.objects.all()
    context={'rooms':rooms,'topics':topics}
    return render(request,'base/home.html',context)

def room(request, room_id):
    room = Room.objects.get(id=room_id)
    context = {'room': room}
    return render(request, 'base/room.html', context)

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

def edit_room(request, room_id):
    room = Room.objects.get(id=room_id)
    # show existance values
    form=RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/collab_form.html', context)

def remove_room(request, room_id):
    room = Room.objects.get(id=room_id)
    # # show existance values
    # form=RoomForm(instance=room)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    # context = {'form': form}
    return render(request, 'base/remove.html', {'obj':room})