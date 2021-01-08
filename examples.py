from django.contrib.auth.models import User

from DungeonCharacter.drd.enums import Races, Profession, Conviction, Size
from DungeonCharacter.drd.models import DrDCharacter
from DungeonCharacter.main.models import Game

game = Game(name='ABC', owner=User.objects.first())
game.save()

char = DrDCharacter(name='Wilson', owner=User.objects.first(), race=Races.HUMAN, profession=Profession.ALCHEMIST,
                    conviction=Conviction.LAWFUL_EVIL, height=1, weigh=1, size=Size.A, level=1, experience=1, strength=1,
                    dexterity=1, immunity=1, intelligence=1, charisma=1, live=1, live_max=1, mag=1, mag_max=1, game=game)

char.save()
