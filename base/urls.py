from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signinPage, name='signin'),
    path('signup/', views.signUpPage, name='signup'),
    path('signout/', views.signOutPage, name='signout'),
    path('', views.home, name='home'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('add-room/', views.add_room, name='add-room'),
    path('edit-room/<int:room_id>', views.edit_room, name='edit-room'),
    path('remove-room/<int:room_id>', views.remove_room, name='remove-room'),


]