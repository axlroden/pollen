import responder
import requests
import json
import sys
from datetime import datetime

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
def east(req, resp):
    date, pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.html = api.template('siri-east.html', last_updated=date, **pollen_data)


@api.route('/siri-west')
def west(req, resp):
    date, pollen_data = render_pollen('https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed')
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.html = api.template('siri-west.html', last_updated=date, **pollen_data)


def render_pollen(feed):
    pollen_values = {}
    try:
        r = requests.get(feed, headers={'accept': 'application/json'})
        feed_values = json.loads(r.json())
        d = datetime.strptime(feed_values["updateTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        update_time = f'{d.day} {d:%B}, {d.year}'
        feed_values_east = feed_values["fields"]["48"]["mapValue"]["fields"]["data"]["mapValue"]["fields"]
        feed_values_west = feed_values["fields"]["49"]["mapValue"]["fields"]["data"]["mapValue"]["fields"]

    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()
        return "", pollen_values

    location = "øst"
    for item in feed_values_east:
        if item == '44' or item == '45':
            continue
        value = feed_values_east[item]["mapValue"]["fields"]["level"]["integerValue"]
        if value == "-1":
            value = "0"
        pollen_values['{0}_{1}'.format(pollen_index[item]["type"], location)] = value
    location = "vest"
    for item in feed_values_west:
        if item == '44' or item == '45':
            continue
        value = feed_values_east[item]["mapValue"]["fields"]["level"]["integerValue"]
        if value == "-1":
            value = "0"
        pollen_values['{0}_{1}'.format(pollen_index[item]["type"], location)] = value
    return update_time, pollen_values


if __name__ == "__main__":
    api.run()
