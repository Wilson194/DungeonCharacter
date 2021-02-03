from django.contrib import admin
from django.contrib.auth import get_user_model

from DungeonCharacter.users.forms import CaseInsensitiveUsernameMixin
from django.contrib.auth.forms import UserChangeForm as ContribUserChangeForm, \
    UserCreationForm as ContribUserCreationForm
from django.contrib.auth.admin import UserAdmin as ContribUserAdmin


class UserChangeForm(CaseInsensitiveUsernameMixin, ContribUserChangeForm):
    pass


class UserCreationForm(CaseInsensitiveUsernameMixin, ContribUserCreationForm):
    pass


class UserAdmin(ContribUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    save_on_top = True


admin.site.register(get_user_model(), UserAdmin)
