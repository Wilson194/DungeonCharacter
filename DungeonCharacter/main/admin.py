from django.contrib import admin

# Register your models here.
from DungeonCharacter.main.models import Game, Bestiary, Chest

admin.site.register(Game)
admin.site.register(Bestiary)
admin.site.register(Chest)
