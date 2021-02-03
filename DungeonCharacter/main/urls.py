from django.urls import path

from DungeonCharacter.main.views import home

urlpatterns = [
    path('', home, name='home'),
]
