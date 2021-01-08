from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'DungeonCharacter.main'


    def ready(self):
        import DungeonCharacter.main.signals
