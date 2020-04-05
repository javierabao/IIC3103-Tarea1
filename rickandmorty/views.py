from django.views.generic import TemplateView

import requests


class IndexView(TemplateView):
    template_name = 'episodes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get('https://rickandmortyapi.com/api/episode')
        res_json = response.json()
        pages = res_json['info']['pages']

        episodes = []
        episodes += res_json['results']

        for page in range(2, pages+1):
            response = requests.get('https://rickandmortyapi.com/api/episode/?page={}'.format(page))
            res_json = response.json()
            episodes += res_json['results']

        context['episodes'] = episodes

        return context


class EpisodeView(TemplateView):
    template_name = 'episodes/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episode_id = kwargs['episode']
        response = requests.get(
            'https://rickandmortyapi.com/api/episode/{}'.format(episode_id)
        )
        episode = response.json()

        context['episode'] = episode
        characters = []

        for character_url in episode['characters']:
            char_response = requests.get(character_url)
            character = char_response.json()
            characters.append(
                {
                    "name": character['name'],
                    "id": character["id"]
                }
            )

        context['characters'] = characters

        return context
