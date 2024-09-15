from django.forms import ModelForm
from .models import Room

# create model form based on the form
class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'