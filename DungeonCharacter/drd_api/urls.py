from django.urls import include, path
from rest_framework import routers

from DungeonCharacter.drd_api import views
from DungeonCharacter.drd_api.routers import DetailOnlyRouter

router = routers.SimpleRouter()
router.register(r'my-characters', views.DrDMyCharacterViewSet, 'drd-my-characters')
router.register(r'character', views.DrDCharacterViewSet, 'drd-character')
router.register(r'my-games', views.DrDGameViewSet, 'drd-my-games')
router.register(r'game-templates', views.DrDGameTemplatesViewSet, 'drd-game-templates')
router.register(r'game-chests', views.DrDGameChestViewSet, 'drd-game-chests')

do_router = DetailOnlyRouter()
do_router.register(r'equipment', views.DrDCharacterEquipmentView, 'equipment')

urlpatterns = [
    path('', views.DocsView.as_view()),
    path('', include(router.urls)),
    path('', include(do_router.urls)),
]
