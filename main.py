import responder
import datetime
import requests

api = responder.API()
last_query = ""
last_updated = ""
# Id is determined from the json feed from dagenspollental website
pollen_index = {
               '1': {'type': 'el'},
               '2': {'type': 'hassel'},
               '4': {'type': 'elm'},
               '7': {'type': 'birk'},
               '28': {'type': 'græs'},
               '31': {'type': 'bynke'}
               }


@api.route('/')
def index(req, resp):
    global last_query
    # Make sure we cache for at least X seconds at a time
    if last_query == "" or last_query < datetime.datetime.now() - datetime.timedelta(minutes=15):
        last_query = datetime.datetime.now()
        last_updated, pollen_values = render_view()
    resp.html = api.template('index.html', last_updated=last_updated, **pollen_values)


def render_view():
    global last_updated
    global pollen_values

    east = requests.get('https://hoefeber.astma-allergi.dk/hoefeber/pollen/dagenspollental?p_p_id=pollenbox_WAR_pollenportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getFeed&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=3&station=48').json() # noqa
    west = requests.get('https://hoefeber.astma-allergi.dk/hoefeber/pollen/dagenspollental?p_p_id=pollenbox_WAR_pollenportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getFeed&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=3&station=49').json() # noqa
    last_updated = east['date']

    pollen_values = {}
    # Combine these 2 at some point when your not lazy. oh and error checking?
    for item in east['feed']:
        # Skip shrooms
        if item == '44' or item == '45':
            continue
        value = east['feed'][item]['level']
        if value == -1:
            value = 0
        pollen_values['{0}_{1}'.format(pollen_index[item]['type'], 'øst')] = value

    for item in west['feed']:
        # Skip shrooms
        if item == '44' or item == '45':
            continue
        value = west['feed'][item]['level']
        if value == -1:
            value = 0
        pollen_values['{0}_{1}'.format(pollen_index[item]['type'], 'vest')] = value

    return last_updated, pollen_values


if __name__ == "__main__":
    api.run()
