import inspect

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import sys


class Game(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    created = models.DateTimeField(editable=False, verbose_name=_('Created'))

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Owner'))

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class Character(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Owner'))
    created = models.DateTimeField(editable=False, verbose_name=_('Created'))

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='%(app_label)s_characters', verbose_name=_('Game'))


    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        clsmembers = {x: y for x, y in inspect.getmembers(sys.modules[self.__module__], inspect.isclass) if
                      issubclass(y, CharacterEquipment) and x != "CharacterEquipment"}
        super().save(*args, **kwargs)

        try:
            list(clsmembers.values())[0](character=self).save()
        except IndexError:
            raise Exception('There is no CharacterEquipment class for module!')


    def __str__(self):
        return f'{self.name} ({self.game.name})'


class Bestiary(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bestiaries', verbose_name=_('Owner'))

    class Meta:
        verbose_name = _('Bestiary')
        verbose_name_plural = _('Bestiaries')

    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class MonsterTemplate(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    bestiary = models.ForeignKey(Bestiary, on_delete=models.CASCADE, related_name='%(app_label)s_monsters',
                                 verbose_name=_('Bestiary'))


    def __str__(self):
        return f'{self.name}'


class Monster(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))


    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    name = models.CharField(max_length=100, null=False, verbose_name=_('Name'))
    description = models.TextField(null=False, verbose_name=_('Description'))
    template = models.BooleanField(null=False, default=False, verbose_name=_('Template'))

    inside = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, related_name='items', blank=True)


    def save(self, *args, **kwargs):
        if self.inside and self.inside.id == self.id:
            raise Exception('Item cannot be contained in itself!')

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name}'


class CharacterEquipment(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='%(app_label)s_equipment',
                                  verbose_name=_('Character'))


    def __str__(self):
        return f"{self.character.name}'s equipment"
