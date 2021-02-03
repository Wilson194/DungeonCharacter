from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from DungeonCharacter.users.models import DungeonUser
from django.utils.translation import ugettext_lazy as _


class CaseInsensitiveUsernameMixin:
    """
    Disallow a username with a case-insensitive match of existing usernames.
    Add this mixin to any forms that use the User object
    """


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username__iexact=username) \
                .exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_(u'The username ‘{}’ is already in use.'.format(username)))
        return username


class UserRegisterForm(CaseInsensitiveUsernameMixin, UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = DungeonUser
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = DungeonUser
        fields = ['username', 'email', 'first_name', 'last_name', 'image']
