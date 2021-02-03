import inspect

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import sys

from DungeonCharacter.main import GAME_MODULES
from DungeonCharacter.main.managers import GameManager
from django.contrib.auth import get_user_model
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Game(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    created = models.DateTimeField(editable=False, verbose_name=_('Created'))
    game_type = models.CharField(choices=[(g.game_id, g.game_name) for g in GAME_MODULES.values()],
                                 verbose_name=_('Game type'), max_length=5)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Owner'), related_name='games')
    invited_users = models.ManyToManyField(get_user_model(), related_name='game_invites')

    image = models.ImageField(default='default_game.png', upload_to='game_pics')

    objects = GameManager()

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    @property
    def characters(self):
        game_type = GAME_MODULES[self.game_type]
        model = game_type.game_app + '.models'

        try:
            clsmembers = {x: y for x, y in inspect.getmembers(sys.modules[model], inspect.isclass) if
                          issubclass(y, Character) and x != 'Character'}
        except IndexError:
            logger.warning(f'No Models in {game_type.game_app} app')
            return Character.objects.filter(game=self)

        if not clsmembers:
            return Character.objects.filter(game=self)

        elif len(clsmembers) > 1:
            logger.error(f'More then one character class found in {game_type.game_app}')
            return None
        else:
            return list(clsmembers.values())[0].objects.filter(game=self)


    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class Character(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    alive = models.BooleanField(verbose_name=_('Alive'), default=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Owner'),
                              related_name='%(app_label)s_characters')

    created = models.DateTimeField(editable=False, verbose_name=_('Created'), auto_now_add=True)
    modified = models.DateTimeField(editable=False, verbose_name=_('Created'), auto_now=True)

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='%(app_label)s_characters',
                             verbose_name=_('Game'))

    image = models.ImageField(default='default_character.png', upload_to='character_pics')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        clsmembers = {x: y for x, y in inspect.getmembers(sys.modules[self.__module__], inspect.isclass) if
                      issubclass(y, CharacterEquipment) and x != "CharacterEquipment"}
        if not hasattr(self, 'characterequipment'):
            try:
                list(clsmembers.values())[0](character=self).save()
            except IndexError:
                raise Exception('There is no CharacterEquipment class for module!')

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def __str__(self):
        return f'{self.name} ({self.game.name})'


class Bestiary(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bestiaries',
                              verbose_name=_('Owner'))

    class Meta:
        verbose_name = _('Bestiary')
        verbose_name_plural = _('Bestiaries')

    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class Chest(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Owner'),
                              related_name='chests',
                              blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name=_('Game'), related_name='chests', blank=True,
                             null=True)
    visible = models.BooleanField(verbose_name=_('Visible'), default=False)


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

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, verbose_name=_('Game'),
                             related_name='item_templates', blank=True)

    inside = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, related_name='items',
                               blank=True, verbose_name=_('Inside'))

    chest = models.ForeignKey(Chest, on_delete=models.CASCADE, null=True, related_name='items', blank=True,
                              verbose_name=_('Chest'))


    def save(self, *args, **kwargs):
        if self.inside and self.inside.id == self.id:
            raise Exception('Item cannot be contained in itself!')

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name}'


class CharacterEquipment(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE,
                                     verbose_name=_('Character'))


    def __str__(self):
        return f"{self.character.name}'s equipment"
