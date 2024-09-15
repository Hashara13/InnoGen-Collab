from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    return render(request,'base/home.html')

def room(request):
    room=None
    for i in rooms:
        if i['id']==int[pk]:
            room=i
    context={'room':room}
    return render(request,'/base/room.html',context)
