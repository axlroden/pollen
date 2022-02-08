import responder
import requests
import sys
from cachetools import cached, TTLCache

api = responder.API()
cache = TTLCache(maxsize=1000, ttl=900)
# Id is determined from the json feed from dagenspollental website
pollen_index = {
               '1': {'type': 'el'},
               '2': {'type': 'hassel'},
               '4': {'type': 'elm'},
               '7': {'type': 'birk'},
               '28': {'type': 'græs'},
               '31': {'type': 'bynke'}
               }


@cached(cache)
@api.route('/')
def index(req, resp):
    pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.html = api.template('index.html', last_updated=pollen_data['48']['date'], **pollen_data)

@cached(cache)
@api.route('/siri-east')
def index(req, resp):
    pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.html = api.template('siri-east.html', last_updated=pollen_data['48']['date'], **pollen_data)

@cached(cache)
@api.route('/siri-west')
def index(req, resp):
    pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.html = api.template('siri-west.html', last_updated=pollen_data['49']['date'], **pollen_data)

@cached(cache)
def render_pollen(feed):
    pollen_values = {}
    try:
        r = requests.get(feed)
        feed_values = r.json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()
        return "", pollen_values
    for item in feed_values:
        if item == '48':
            location = 'øst'
        elif item == '49':
            location = 'vest'
        else:
            location = ''
        for pollen in item['data']:
            value = pollen['level']
            if value == -1:
                value = "0"
            pollen_values['{0}_{1}'.format(pollen_index[pollen]['type'], location)] = value
    return pollen_values

if __name__ == "__main__":
    api.run()
