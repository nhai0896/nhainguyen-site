from django.urls import path
from . import views

app_name = 'sms'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
]
