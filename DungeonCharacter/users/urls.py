from django.urls import path, include
from DungeonCharacter.users import views as user_views
from django.contrib.auth import views as auth_views

from DungeonCharacter.users.views import CharacterListView, GameListView

urlpatterns = [
    path('', user_views.profile, name='profile'),
    path('register/', user_views.register, name='register'),
    # path('profile/friends/', user_views.friend_list, name='profile_friends'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('characters/', CharacterListView.as_view(), name='characters'),
    path('games/', GameListView.as_view(), name='games'),

    # path('user/<str:username>/', profile_public, name='profile_public'),
    # path('user/<str:username>/friend-add', friend_add, name='friend_add'),
    # path('user/<str:username>/friend-remove', friend_remove, name='friend_remove'),
    # path('user/<str:username>/friend-confirm', friend_confirm, name='friend_confirm'),

    # path('ajax/search_users/', ajax_user_search, name='ajax_user_search'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
