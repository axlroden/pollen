from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
import uvicorn
import requests
import json
import sys
from datetime import datetime

# Id is determined from the json feed from dagenspollental website
pollen_index = {
    '1': {'type': 'el'},
    '2': {'type': 'hassel'},
    '4': {'type': 'elm'},
    '7': {'type': 'birk'},
    '28': {'type': 'græs'},
    '31': {'type': 'bynke'}
}
feed = 'https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed'

templates = Jinja2Templates(directory="templates")

async def index(request):
    date, pollen_data = render_pollen(feed)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    content = templates.TemplateResponse("index.html",
                                         {"request": request, "last_updated": date, **pollen_data},
                                         headers=headers)
    return content


async def east(request):
    date, pollen_data = render_pollen(feed)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    content = templates.TemplateResponse("siri-east.html",
                                         {"request": request, "last_updated": date, **pollen_data},
                                         headers=headers)
    return content

async def west(request):
    date, pollen_data = render_pollen(feed)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    content = templates.TemplateResponse("siri-west.html",
                                         {"request": request, "last_updated": date, **pollen_data},
                                         headers=headers)
    return content

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
        value = feed_values_west[item]["mapValue"]["fields"]["level"]["integerValue"]
        if value == "-1":
            value = "0"
        pollen_values['{0}_{1}'.format(pollen_index[item]["type"], location)] = value
    return update_time, pollen_values


routes = [
    Route('/', index),
    Route('/siri-east', east),
    Route('/siri-west', west),
    Mount('/static', app=StaticFiles(directory='static'), name="static"),
]
app = Starlette(debug=True, routes=routes)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
