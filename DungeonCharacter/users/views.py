from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView, ListView

from DungeonCharacter.main.models import Character, Game
from DungeonCharacter.users.models import DungeonUser
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'users/profile.html', context)


class CharacterListView(ListView):
    model = Character
    template_name = 'users/characters.html'
    context_object_name = 'characters'


    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user).order_by('modified')


class GameListView(ListView):
    model = Game
    template_name = 'users/games.html'
    context_object_name = 'games'


    def get_queryset(self):
        return Game.objects.games(self.request.user)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        characters = {}
        for game in context['games']:
            g_characters = game.characters.filter(Q(owner=self.request.user) & Q(alive=True))
            characters[game.id] = None if g_characters is None else g_characters.first()

        context['characters'] = characters
        return context
