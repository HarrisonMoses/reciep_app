'''
Urls for the user app.
'''
from django.urls import path

from user import views

app_name = 'user'  

ulrpatterns =[
    path('create/',views.CreateUserView.as_view(), name='create_user'),
]