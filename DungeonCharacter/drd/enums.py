from django.db import models
from django.utils.translation import gettext_lazy as _


class Races(models.TextChoices):
    HUMAN = 'HU', _('Human')
    DWARF = 'DW', _('Dwarf')
    ELF = 'EL', _('Elf')
    KROLL = 'KR', _('Kroll')
    KUDUK = 'KD', _('Kuduk')
    BARBAR = 'BA', _('Barbar')
    HOBBIT = 'HO', _('Hobbit')


class Profession(models.TextChoices):
    WARRIOR = 'WAR', _('Warrior')
    GUARD = 'GUA', _('Guard')
    WIZARD = 'WIZ', _('Wizard')
    THIEF = 'THI', _('Thief')
    ALCHEMIST = 'ALCH', _('Alchemist')


class Conviction(models.TextChoices):
    LAWFUL_GOOD = 'LG', _('Lawful good')
    CONFUSED_GOODNESS = 'CG', _('Confused goodness')
    NEUTRAL = 'NE', _('Neutral')
    CONFUSED_EVIL = 'CE', _('Confused evil')
    LAWFUL_EVIL = 'LE', _('Lawful evil')


class Size(models.TextChoices):
    A0 = 'A0',
    A = 'A',
    B = 'B',
    C = 'C',
    D = 'D',
    E = 'E',
    F = 'F',


class MonsterClass(models.TextChoices):
    HUMANOID = 'HUM', _('Humanoid')
    ANIMAL = 'ANI', _('Animal')
    BEAST = 'BEA', _('Best')
    DRAGON = 'DRA', _('Dragon')
    REPTILE = 'REP', _('Reptile')
    INSECT = 'INS', _('Insect')
    AQUATIC_CREATURES = 'AQC', _('Aquatic creature')
    WINGED = 'WNG', _('Winged')
    MAGIC_CREATURES = 'MGC', _('Magic creature')


class WeaponWeightType(models.TextChoices):
    LIGHT = 'LIG', _('Light')
    MIDDLE = 'MID', _('Middle')
    HEAVY = 'HEA', _('Heavy')
