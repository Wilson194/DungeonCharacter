from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import Q


class GameManager(models.Manager):
    def games(self, user, order=('id',)):
        from DungeonCharacter.main.models import Character, Game

        if user is None or user is AnonymousUser:
            return None

        q = Q(owner=user)
        q2 = Q(invited_users=user)

        return Game.objects.filter(q | q2).order_by(*order)
