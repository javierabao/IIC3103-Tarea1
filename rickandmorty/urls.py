from django.urls import path

from .views import IndexView, EpisodeView, CharacterView

urlpatterns = [
    path('', IndexView.as_view(), name='episode_list'),
    path(
        'episodes/<int:episode>/',
        EpisodeView.as_view(),
        name='episode_detail'
    ),
    path(
        'characters/<int:character>/',
        CharacterView.as_view(),
        name='character_detail'
    )
]
