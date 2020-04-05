from django.urls import path

from .views import IndexView, EpisodeView, CharacterView, LocationView, SearchView

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
    ),
    path(
        'locations/<int:location>/',
        LocationView.as_view(),
        name='location_detail'
    ),
    path(
        'search/',
        SearchView.as_view(),
        name='search_results'
    )
]
