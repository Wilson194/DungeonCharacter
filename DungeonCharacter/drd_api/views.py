from django.shortcuts import render
from collections import defaultdict
from django.utils.translation import gettext as _
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from DungeonCharacter.drd.models import DrDCharacter, DrDCharacterEquipment, DrDItem
from DungeonCharacter.drd_api.serializers import DrDCharacterSerializer, DrDCharacterEquipmentSerializer, \
    DrDGameSerializer, resolve_item_type, DrDChestSerializer
from DungeonCharacter.main.models import Game, Chest
from DungeonCharacter.main.permissions import CharacterPermission


class DrDMyCharacterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DrDCharacterSerializer


    def get_queryset(self):
        user = self.request.user
        print(user, type(user))
        return DrDCharacter.objects.filter(owner=user)


class DrDCharacterViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = DrDCharacterSerializer
    permission_classes = [CharacterPermission]


    def get_queryset(self):
        return DrDCharacter.objects.all()


class DrDCharacterEquipmentView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = DrDCharacterEquipmentSerializer


    def get_queryset(self):
        user = self.request.user
        return DrDCharacterEquipment.objects.filter(character__owner=user)


class DrDGameViewSet(viewsets.ModelViewSet):
    serializer_class = DrDGameSerializer


    def get_queryset(self):
        user = self.request.user
        return Game.objects.filter(owner=user)


class DrDGameTemplatesViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')

        items = DrDItem.objects.filter(game__pk=pk)
        result = defaultdict(list)

        for item in items:
            item = resolve_item_type(item)
            result[item.Meta.model.__name__].append(item.data)

        return Response(result)


class DrDGameChestViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        return Game.objects.all()


    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')

        chests = Chest.objects.filter(game__pk=pk)

        return Response([DrDChestSerializer(chest).data for chest in chests])


class DocsView(APIView):

    def get(self, request, *args, **kwargs):
        apidocs = {
            _('My characters'): request.build_absolute_uri('my-characters'),
            _('Character'): request.build_absolute_uri('character/pk'),
            _('My games'): request.build_absolute_uri('my-games'),
            _('Game templates'): request.build_absolute_uri('game-templates/pk'),
            _('Game chests'): request.build_absolute_uri('game-chests/pk')
        }

        return Response(apidocs)
