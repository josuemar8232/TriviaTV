import os

import requests
from pathlib import Path

from requests_oauthlib import OAuth2Session


class PhotosController:
    def generate_photos(self, query, file_name):
        url = 'https://www.googleapis.com/customsearch/v1'
        search_key = os.environ.get("GOOGLE_SEARCH_KEY")
        if not search_key:
            raise EnvironmentError(
                "GOOGLE_SEARCH_KEY environment variable is not set")
        search_engine_id = os.environ.get("SEARCH_ENGINE_ID")
        if not search_engine_id:
            raise EnvironmentError(
                "SEARCH_ENGINE_ID environment variable is not set")

        params = {
            'q': query,
            'key': search_key,
            'cx': search_engine_id,
            'searchType': 'image',
            'image_sort_by': '',
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()['items']

        if results:
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            photos_file_path = project_root / "data" / "photos"

            photo_url = results[0]['link']
            response = requests.get(photo_url)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                photo_url = results[1]['link']
                response = requests.get(photo_url)

            final_file_name = f"{file_name}.jpg"
            # Generating a unique filename
            photo_path = photos_file_path / final_file_name

            with open(photo_path, "wb") as file:
                file.write(response.content)

    def generate_photo_with_text(self, query):
        url = 'https://api.unsplash.com/search/photos'
        unsplash_key = os.environ.get("UNSPLASH_KEY")
        if not unsplash_key:
            raise EnvironmentError(
                "UNSPLASH_KEY environment variable is not set")

        params = {
            'query': query,
            'per_page': 1,
            'orientation': 'portrait',
            'client_id': unsplash_key
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()['results']
        if results:
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            photos_file_path = project_root / "data" / "photos"

            photo_url = results[0]['urls']['regular']
            response = requests.get(photo_url)
            response.raise_for_status()

            file_name = f"{query.replace(' ', '_')}.jpg"
            # Generating a unique filename
            photo_path = photos_file_path / file_name

            with open(photo_path, "wb") as file:
                file.write(response.content)

    def generate_photo_with_shutterstock(self, query):
        url = 'https://api.shutterstock.com/v2/images/search'
        shutterstock_key = os.environ.get("SHUTTERSTOCK_KEY")
        if not shutterstock_key:
            raise EnvironmentError(
                "SHUTTERSTOCK_KEY environment variable is not set")

        shutterstock_token = os.environ.get("SHUTTERSTOCK_TOKEN")
        if not shutterstock_token:
            raise EnvironmentError(
                "SHUTTERSTOCK_TOKEN environment variable is not set")

        params = {
            'query': query,
            'sort': 'relevance',
            'per_page': '1',
            # 'orientation': 'vertical',
            'client_id': shutterstock_key
        }

        session = OAuth2Session()
        session.headers['Authorization'] = f'Bearer {shutterstock_token}'

        response = session.get(url, params=params)
        response.raise_for_status()
        results = response.json()['data']
        if results:
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            photos_file_path = project_root / "data" / "photos"

            photo_url = results[0]['assets']['preview_1500']['url']
            response = requests.get(photo_url)
            response.raise_for_status()

            file_name = f"{query.replace(' ', '_')}.jpg"
            # Generating a unique filename
            photo_path = photos_file_path / file_name

            with open(photo_path, "wb") as file:
                file.write(response.content)

    def add_photo_to_video(self):
        pass
