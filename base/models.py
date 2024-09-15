from django.db import models

class Room(models.Model):
    # host=
    # owner=
    # topic=
    name=models.CharField(max_length=300)
    desc=models.TextField(max_length=800,null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name