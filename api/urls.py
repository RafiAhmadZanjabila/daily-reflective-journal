from django.urls import path
from .views import emotion_list

urlpatterns = [
    path('emotions/', emotion_list, name='emotion-list')
]
