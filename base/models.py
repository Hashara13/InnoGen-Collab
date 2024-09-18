from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name=models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=300)
    desc=models.TextField(max_length=800,null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateField(auto_now_add=True)
    
    # sort recent in fIrst
    class Meta:
        ordering=['-updated','-created']
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    
     # once delete 1 user contain messages also deleted
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # once delete 1 chat room contain messages also deleted
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateField(auto_now_add=True)
    
    def __str__(self):
        # view 1st 50 characters
        return self.body[0:50]