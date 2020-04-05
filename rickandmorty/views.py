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
            response = requests.get(
                'https://rickandmortyapi.com/api/episode/?page={}'
                .format(page)
            )
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


class CharacterView(TemplateView):
    template_name = 'characters/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character_id = kwargs['character']
        response = requests.get(
            'https://rickandmortyapi.com/api/character/{}'.format(character_id)
        )
        character = response.json()

        context['character'] = character

        context['origin'] = {
            "id": int(
                character['origin']['url'].split("/")[-1]
            ) if character['origin']['url'].split("/")[-1] else '',
            "name": character['origin']['name']
        }

        context['location'] = {
            "id": int(
                character['location']['url'].split("/")[-1]
            ) if character['location']['url'].split("/")[-1] else '',
            "name": character['location']['name']
        }

        episodes = []

        for episode_url in character['episode']:
            epi_response = requests.get(episode_url)
            episode = epi_response.json()
            episodes.append(
                {
                    "episode": episode['episode'],
                    "name": episode['name'],
                    "id": episode["id"]
                }
            )

        context['episodes'] = episodes

        return context


class LocationView(TemplateView):
    template_name = 'locations/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = kwargs['location']
        response = requests.get(
            'https://rickandmortyapi.com/api/location/{}'.format(location_id)
        )
        location = response.json()

        context['location'] = location

        residents = []

        for resident_url in location['residents']:
            res_response = requests.get(resident_url)
            resident = res_response.json()
            residents.append(
                {
                    "name": resident['name'],
                    "id": resident["id"]
                }
            )

        context['residents'] = residents

        return context


class SearchView(TemplateView):
    template_name = 'search/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_str = self.request.GET.get('search_str')

        epi_response = requests.get(
            'https://rickandmortyapi.com/api/episode/?name={}'
            .format(search_str)
        ).json()
        char_response = requests.get(
            'https://rickandmortyapi.com/api/character/?name={}'
            .format(search_str)
        ).json()
        loc_response = requests.get(
            'https://rickandmortyapi.com/api/location/?name={}'
            .format(search_str)
        ).json()

        context['episodes'] = (
            epi_response['results'] if 'results' in epi_response
            else []
        )
        context['characters'] = (
            char_response['results'] if 'results' in char_response
            else []
        )
        context['locations'] = (
            loc_response['results'] if 'results' in loc_response
            else []
        )

        return context
