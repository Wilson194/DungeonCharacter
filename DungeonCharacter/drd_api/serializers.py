from rest_framework import serializers
from rest_framework.reverse import reverse
from DungeonCharacter.drd.models import DrDCharacter, DrDCharacterEquipment, DrDItem, DrDContainer, DrDWeapon, \
    DrDAmmunition, DrDRangeWeapon, DrDArmor
from DungeonCharacter.main.models import Game, Chest


def resolve_item_type(item):
    types = {
        'drdcontainer': DrDContainerSerializer,
        'drdammunition': DrDAmmunitionSerializer,
        'drdweapon': DrDWeaponSerializer,
        'drdrangeweapon': DrDRangeWeaponSerializer,
        'drdarmor': DrDArmorSerializer,
        'drditem': DrDItemSerializer,
    }

    for name, cls in types.items():
        if hasattr(item, name):
            return cls(getattr(item, name))


class DrDItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = DrDItem
        fields = ['name', 'description', 'weight', 'price', 'quantity', 'items']

    def get_items(self, instance):
        items = []
        for item in instance.items.all():
            item = resolve_item_type(item)
            if item is not None:
                items.append(item.data)
        return items


class DrDAmmunitionSerializer(DrDItemSerializer):
    class Meta(DrDItemSerializer.Meta):
        model = DrDAmmunition
        fields = DrDItemSerializer.Meta.fields + ['strength']


class DrDWeaponSerializer(DrDItemSerializer):
    class Meta(DrDItemSerializer.Meta):
        model = DrDWeapon
        fields = DrDItemSerializer.Meta.fields + ['strength', 'rampancy', 'defense', 'length',
                                                  'weight_type', 'one_handed']


class DrDRangeWeaponSerializer(DrDItemSerializer):
    class Meta(DrDItemSerializer.Meta):
        model = DrDRangeWeapon
        fields = DrDItemSerializer.Meta.fields + ['strength', 'rampancy', 'range_short',
                                                  'range_middle', 'range_far', 'throwing']


class DrDArmorSerializer(DrDItemSerializer):
    class Meta(DrDItemSerializer.Meta):
        model = DrDArmor
        fields = DrDItemSerializer.Meta.fields + ['quality']


class DrDContainerSerializer(DrDItemSerializer):
    class Meta(DrDItemSerializer.Meta):
        model = DrDContainer
        fields = DrDItemSerializer.Meta.fields + ['capacity']


class DrDCharacterEquipmentSerializer(serializers.ModelSerializer):
    character_name = serializers.SerializerMethodField()
    character = serializers.SerializerMethodField()
    left_hand = serializers.SerializerMethodField()
    right_hand = serializers.SerializerMethodField()
    head = serializers.SerializerMethodField()
    torso = serializers.SerializerMethodField()
    back = serializers.SerializerMethodField()
    hands = serializers.SerializerMethodField()
    belt = serializers.SerializerMethodField()
    legs = serializers.SerializerMethodField()
    feet = serializers.SerializerMethodField()

    class Meta:
        model = DrDCharacterEquipment
        fields = ['id', 'character_name', 'character', 'left_hand', 'right_hand', 'head', 'torso', 'back', 'hands',
                  'belt', 'legs', 'feet']

        depth = 10

    def get_character(self, instance):
        return reverse('drd-character-detail', args=[instance.character.id],
                       request=self.context['request'])


    def get_character_name(self, instance):
        return instance.character.name


    def get_left_hand(self, instance):
        serializer = resolve_item_type(instance.left_hand)
        return serializer.data if serializer else None


    def get_right_hand(self, instance):
        serializer = resolve_item_type(instance.right_hand)
        return serializer.data if serializer else None


    def get_head(self, instance):
        serializer = resolve_item_type(instance.head)
        return serializer.data if serializer else None


    def get_torso(self, instance):
        serializer = resolve_item_type(instance.torso)
        return serializer.data if serializer else None


    def get_back(self, instance):
        serializer = resolve_item_type(instance.back)
        return serializer.data if serializer else None


    def get_hands(self, instance):
        serializer = resolve_item_type(instance.hands)
        return serializer.data if serializer else None


    def get_belt(self, instance):
        serializer = resolve_item_type(instance.belt)
        return serializer.data if serializer else None


    def get_legs(self, instance):
        serializer = resolve_item_type(instance.legs)
        return serializer.data if serializer else None


    def get_feet(self, instance):
        serializer = resolve_item_type(instance.feet)
        return serializer.data if serializer else None


class DrDCharacterSerializer(serializers.ModelSerializer):
    game_name = serializers.SerializerMethodField()
    equipment = serializers.SerializerMethodField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game_id'] = serializers.ChoiceField(
            choices=[(obj.id, obj.name) for obj in Game.objects.filter(invited_users=self.context['request'].user)])

    class Meta:
        model = DrDCharacter
        fields = ['id', 'name', 'description', 'created', 'race', 'profession', 'conviction', 'height', 'weigh', 'size',
                  'level', 'experience', 'strength', 'dexterity', 'immunity', 'intelligence', 'charisma', 'live',
                  'live_max', 'mag', 'mag_max', 'game_id', 'game_name', 'equipment', 'owner']

        depth = 3

    def get_game_name(self, instance):
        return instance.game.name


    def get_equipment(self, instance):
        return reverse('equipment-detail', args=[instance.characterequipment.drdcharacterequipment.id],
                       request=self.context['request'])


class DrDGameSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    characters = serializers.SerializerMethodField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Game
        fields = '__all__'

    def get_owner_name(self, instance):
        return str(instance.owner)


    def get_characters(self, instance):
        return {obj.name: reverse('drd-character-detail', args=[obj.id],
                                  request=self.context['request']) for obj in instance.characters.all()}


class DrDChestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chest
        fields = '__all__'
