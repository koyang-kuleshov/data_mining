import requests
from datetime import datetime as dt
import json


SPECIAL_URL = 'https://5ka.ru/api/v2/special_offers/'
CATEGORIES_URL = 'https://5ka.ru/api/v2/categories/'
params = {
    'record_per_page': 20,
    }

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64; rv:68.0)'
                   ' Gecko/20100101 Firefox/68.0'),
    'Referer': 'https://5ka.ru/special_offers/'
          }


class CatalogByCategory:

    def __init__(self, cat_url, spec_url, headers, params):
        self.__cat_url = cat_url
        self.__spec_url = spec_url
        self.__headers = headers
        self.__params = params

    def get_data_from_api(self):
        try:
            response = requests.get(self.__cat_url,
                                    headers=self.__headers,
                                    params=self.__params)
        except Exception as err:
            print(f'Fetching categories failed: {err}')
            return None
        else:
            categories = response.json()

        for cat in categories:
            self.__params["categories"] =\
                f'{cat["parent_group_code"]}'
            try:
                response = requests.get(
                    self.__spec_url,
                    headers=self.__headers,
                    params=self.__params)
            except Exception as err:
                print(err)
            else:
                data = response.json()['results']
                if data:
                    self.save_json_to_file(cat["parent_group_name"],
                                           response.json()['results'])

    def save_json_to_file(self, group_name, data):
        file_name = group_name.replace(' ', '-').replace(',', '')
        file_name = file_name + '-' + dt.now().strftime('%d-%m-%Y-%H-%M')\
            + '.json'
        try:
            with open(file_name, 'w', encoding='UTF-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False)
        except Exception as err:
            print(err)


if __name__ == "__main__":
    catalog = CatalogByCategory(CATEGORIES_URL, SPECIAL_URL, HEADERS, params)
    catalog.get_data_from_api()
