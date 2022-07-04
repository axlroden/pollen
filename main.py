import responder
import requests
import json
import sys

api = responder.API()
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
    date, pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.html = api.template('index.html', last_updated=date, **pollen_data)

@api.route('/siri-east')
def index(req, resp):
    date, pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.html = api.template('siri-east.html', last_updated=date, **pollen_data)

@api.route('/siri-west')
def index(req, resp):
    date, pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.html = api.template('siri-west.html', last_updated=date, **pollen_data)

def render_pollen(feed):
    pollen_values = {}
    try:
        r = requests.get(feed)
        feed_values = json.loads(r.json())

    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()
        return "", pollen_values
    
    location = "øst"
    for item in feed_values["48"]["data"]:
        if item == '44' or item == '45':
            continue
        value = feed_values["48"]["data"][item]['level']
        if value == -1:
            value = "0"
        pollen_values['{0}_{1}'.format(pollen_index[item]["type"], location)] = value
    location = "vest"
    for item in feed_values["49"]["data"]:
        if item == '44' or item == '45':
            continue
        value = feed_values["49"]["data"][item]['level']
        if value == -1:
            value = "0"
        pollen_values['{0}_{1}'.format(pollen_index[item]["type"], location)] = value
    return feed_values["48"]["date"], pollen_values

if __name__ == "__main__":
    api.run()
