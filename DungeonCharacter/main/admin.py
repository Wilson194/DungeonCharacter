from django.contrib import admin

# Register your models here.
from DungeonCharacter.main.models import Game, Bestiary

admin.site.register(Game)
admin.site.register(Bestiary)
