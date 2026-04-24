import requests

GEOCODER_API_KEY = '7eb1332d-4876-4b40-b314-76834f59eef7'
STATICMAP_API_KEY = 'ed983e3f-c780-4aab-9899-589fda08af66'

GEOCODER_URL = 'https://geocode-maps.yandex.ru/1.x/'
STATICMAP_URL = 'https://static-maps.yandex.ru/v1'


def get_city_coords(city: str):
    params = {'apikey': GEOCODER_API_KEY, 'geocode': city, 'format': 'json', 'results': 1}
    try:
        resp = requests.get(GEOCODER_URL, params=params, timeout=5)
        print(resp.url)
        resp.raise_for_status()
        data = resp.json()
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = map(float, pos.split())
        print(lon, lat)
        return lon, lat
    except (KeyError, IndexError, requests.RequestException):
        return None


def get_map_url(city: str, zoom: int = 12):
    coords = get_city_coords(city)
    if coords is None:
        return None
    lon, lat = coords
    params = {'apikey': STATICMAP_API_KEY, 'll': f'{lon},{lat}', 'z': zoom}
    req = requests.PreparedRequest()
    req.prepare_url(STATICMAP_URL, params)
    return req.url
