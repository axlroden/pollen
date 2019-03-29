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
    last_updated, east = render_pollen('øst', 'https://hoefeber.astma-allergi.dk/hoefeber/pollen/dagenspollental?p_p_id=pollenbox_WAR_pollenportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getFeed&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=3&station=48') # noqa
    last_updated, west = render_pollen('vest', 'https://hoefeber.astma-allergi.dk/hoefeber/pollen/dagenspollental?p_p_id=pollenbox_WAR_pollenportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getFeed&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=3&station=49') # noqa
    # Merge dictionaries
    pollen_values = {**west, **east}
    resp.html = api.template('index.html', last_updated=last_updated, **pollen_values)


@cached(cache)
def render_pollen(location, feed):
    pollen_values = {}
    try:
        r = requests.get(feed).json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()
        return "", pollen_values

    for item in r['feed']:
        # Skip shrooms
        if item == '44' or item == '45':
            continue
        value = r['feed'][item]['level']
        if value == -1:
            value = "-"
        pollen_values['{0}_{1}'.format(pollen_index[item]['type'], location)] = value
    return r['date'], pollen_values


if __name__ == "__main__":
    api.run()
