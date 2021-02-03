from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractUser
from PIL import Image


class DungeonUserUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class DungeonUser(AbstractUser):
    objects = DungeonUserUserManager()
    image = models.ImageField(default='default.png', upload_to='profile_pics/')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)