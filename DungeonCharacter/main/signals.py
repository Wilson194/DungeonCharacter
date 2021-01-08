# import inspect
# import sys
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from DungeonCharacter.main.models import Character
#
#
# @receiver(post_save)
# def search_on_post_save(sender, instance, **kwargs):
#     if issubclass(sender, Character):
#         print(sender, instance)
#         clsmembers = {x: y for x, y in inspect.getmembers(sys.modules[self.__module__], inspect.isclass) if
#                       issubclass(y, CharacterEquipment) and x != "CharacterEquipment"}
#         print(clsmembers)
