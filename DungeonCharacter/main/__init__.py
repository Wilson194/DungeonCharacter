import importlib

from django.conf import settings

default_app_config = 'DungeonCharacter.main.apps.MainConfig'


class GameModule:
    def __init__(self, game_id, game_name, game_app):
        if len(str(game_id)) > 5:
            raise ValueError('Maximum length of Game id is 5!')
        self.game_id = game_id
        self.game_name = game_name
        self.game_app = game_app


GAME_MODULES = {}
for app in settings.INSTALLED_APPS:
    try:
        module = importlib.import_module(app)
        GAME_MODULES[module.GAME_TYPE_ID] = GameModule(module.GAME_TYPE_ID, module.GAME_TYPE_NAME, app)
    except AttributeError:
        pass
