from django.db import models

from DungeonCharacter.drd.enums import Races, Profession, Conviction, Size, MonsterClass, WeaponWeightType
from DungeonCharacter.main.models import Character, MonsterTemplate, CharacterEquipment, Item
from django.utils.translation import gettext_lazy as _


class DrDCharacter(Character):
    race = models.CharField(max_length=2, choices=Races.choices, null=False, verbose_name=_('Race'))
    profession = models.CharField(max_length=4, choices=Profession.choices, null=False, verbose_name=_('Profession'))

    # Description
    conviction = models.CharField(max_length=2, choices=Conviction.choices, null=False, verbose_name=_('Conviction'))
    height = models.IntegerField(null=False, verbose_name=_('Height'))
    weigh = models.IntegerField(null=False, verbose_name=_('Weigh'))
    size = models.CharField(max_length=2, choices=Size.choices, null=False, verbose_name=_('Size'))

    # Experience
    level = models.IntegerField(null=False, default=1, verbose_name=_('Level'))
    experience = models.IntegerField(null=False, default=0, verbose_name=_('Experience'))

    # Attributes
    strength = models.IntegerField(null=False, verbose_name=_('Strength'))
    dexterity = models.IntegerField(null=False, verbose_name=_('Dexterity'))
    immunity = models.IntegerField(null=False, verbose_name=_('Immunity'))
    intelligence = models.IntegerField(null=False, verbose_name=_('Intelligence'))
    charisma = models.IntegerField(null=False, verbose_name=_('Charisma'))

    # Live
    live = models.IntegerField(null=False, verbose_name=_('Live current'))
    live_max = models.IntegerField(null=False, verbose_name=_('Live maximum'))

    # Mana
    mag = models.IntegerField(null=False, verbose_name=_('Mag current'))
    mag_max = models.IntegerField(null=False, verbose_name=_('Mag maximum'))

    class Meta:
        verbose_name = _("Character")
        verbose_name_plural = _("Characters")

    def __str__(self):
        return 'DrDCharacter'




class DrDMonsterKind(MonsterTemplate):
    viability = models.FloatField(null=False, verbose_name=_('Viability'))

    # TODO: Upravit
    attack = models.IntegerField(null=False, verbose_name=_('Attack'))

    dexterity = models.IntegerField(null=False, verbose_name=_('Dexterity'))
    basic_defense = models.IntegerField(null=False, verbose_name=_('Basic defense'))

    endurance = models.IntegerField(null=False, verbose_name=_('Endurance'))
    size = models.CharField(max_length=2, null=False, choices=Size.choices, verbose_name=_('Size'))
    pugnacity = models.IntegerField(null=False, verbose_name=_('Pugnacity'))

    # TODO: Zranitelnost

    mobility_type = models.CharField(max_length=3, null=False, choices=MonsterClass.choices,
                                     verbose_name=_('Mobility type'))
    mobility = models.IntegerField(null=False, verbose_name=_('Mobility'))

    perseverance_type = models.CharField(max_length=3, null=False, choices=MonsterClass.choices,
                                         verbose_name=_('Perseverance type'))
    perseverance = models.IntegerField(null=False, verbose_name=_('Perseverance'))

    intelligence = models.IntegerField(null=False, verbose_name=_('Intelligence'))
    experience = models.IntegerField(null=False, verbose_name=_('Experience'))

    class Meta:
        verbose_name = _("Monster kind")
        verbose_name_plural = _("Monster kinds")


class DrDMonsterAttack(models.Model):
    name = models.CharField(null=False, max_length=100, verbose_name=_('Name'))
    monster = models.ForeignKey(DrDMonsterKind, on_delete=models.CASCADE, verbose_name='attacks')

    aggression = models.IntegerField(null=False, verbose_name=_('Aggression'))
    attack = models.IntegerField(null=False, verbose_name=_('Attack number'))
    default_weapon_attack = models.IntegerField(null=True, verbose_name=_('Default weapon attack'))

    possible_weapon = models.BooleanField(default=False, verbose_name=_('Could use weapon'))

    class Meta:
        verbose_name = _("Monster attack")
        verbose_name_plural = _("Monster attacks")


class DrDItem(Item):
    weight = models.IntegerField(null=False, verbose_name=_('Weigh'))
    price = models.IntegerField(null=False, verbose_name=_('Price'))
    quantity = models.IntegerField(default=1, verbose_name=_('Quantity'))

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class DrDAmmunition(DrDItem):
    strength = models.IntegerField(null=False, verbose_name=_('Strength'))

    class Meta:
        verbose_name = _('Ammunition')
        verbose_name_plural = _('Ammunition')


class DrDWeapon(DrDItem):
    strength = models.IntegerField(null=False, verbose_name=_('Strength'))
    rampancy = models.IntegerField(null=False, verbose_name=_('Rampancy'))
    defense = models.IntegerField(null=False, verbose_name=_('Defense'))
    length = models.IntegerField(null=False, verbose_name=_('Length'))

    weight_type = models.CharField(max_length=3, choices=WeaponWeightType.choices, verbose_name=_('Weight type'))
    one_handed = models.BooleanField(null=False, verbose_name=_('One handed'))

    class Meta:
        verbose_name = _("Weapon")
        verbose_name_plural = _("Weapons")


class DrDRangeWeapon(DrDItem):
    strength = models.IntegerField(null=False, verbose_name=_('Strength'))
    rampancy = models.IntegerField(null=False, verbose_name=_('Rampancy'))
    range_short = models.IntegerField(null=False, verbose_name=_('Range short'))
    range_middle = models.IntegerField(null=False, verbose_name=_('Range middle'))
    range_far = models.IntegerField(null=False, verbose_name=_('Range far'))
    throwing = models.BooleanField(null=False, default=False, verbose_name=_('Throwing'))

    class Meta:
        verbose_name = _("Range weapon")
        verbose_name_plural = _("Range weapons")


class DrDArmor(DrDItem):
    quality = models.IntegerField(null=False, verbose_name=_('Quality'))

    class Meta:
        verbose_name = _("Armor")
        verbose_name_plural = _("Armors")


class DrDContainer(DrDItem):
    capacity = models.IntegerField(null=True, verbose_name=_('Capacity'))

    class Meta:
        verbose_name = _("Container")
        verbose_name_plural = _("Containers")

    @property
    def contained_weight(self) -> int:
        _sum = 0
        for item in self.items:
            if issubclass(item, DrDContainer):
                _sum += item.weight + item.contained_weight
            else:
                _sum += item.weight
        return _sum


class DrDCharacterEquipment(CharacterEquipment):
    left_hand = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Left hand'),
                                  related_name='+', blank=True)
    right_hand = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Right hand'),
                                   related_name='+', blank=True)

    head = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Head'), related_name='+',
                             blank=True)
    torso = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Torso'), related_name='+',
                              blank=True)
    back = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Back'), related_name='+',
                             blank=True)
    hands = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Hands'), related_name='+',
                              blank=True)
    belt = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Belt'), related_name='+',
                             blank=True)
    legs = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Legs'), related_name='+',
                             blank=True)
    feet = models.ForeignKey(DrDItem, on_delete=models.SET_NULL, null=True, verbose_name=_('Feet'), related_name='+',
                             blank=True)

    class Meta:
        verbose_name = _('Character equipment')
        verbose_name_plural = _('Character equipments')

    def __str__(self):
        return 'DrDCharacterEquipment'
