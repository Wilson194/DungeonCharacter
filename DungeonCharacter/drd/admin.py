from django.contrib import admin

# Register your models here.
from DungeonCharacter.drd.models import DrDMonsterKind, DrDItem, DrDArmor, DrDWeapon, DrDRangeWeapon, DrDMonsterAttack, \
    DrDCharacter, DrDCharacterEquipment, DrDContainer

admin.site.register(DrDCharacter)
admin.site.register(DrDMonsterKind)
admin.site.register(DrDItem)
admin.site.register(DrDArmor)
admin.site.register(DrDWeapon)
admin.site.register(DrDRangeWeapon)
admin.site.register(DrDMonsterAttack)
admin.site.register(DrDCharacterEquipment)
admin.site.register(DrDContainer)
