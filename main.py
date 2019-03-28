import responder
import datetime
import time
import tweepy
from tweepy import OAuthHandler
from dynaconf import settings

api = responder.API()
last_query = ""
last_consume = ""
pollentypes = ['el', 'hassel', 'elm', 'birk', 'græs', 'bynke']
pollendic = []

@api.route('/')
def index(req, resp):
    global last_query
    global last_updated
    global pollen_values
    last_updated = ""
    if last_query == "":
        # Make sure we have some data.
        check_twitter()
    # Make sure we cache for at least X seconds at a time
    if last_query == "" or last_query < datetime.datetime.now() - datetime.timedelta(minutes=settings.CACHE_TIMER):
        last_query = datetime.datetime.now()
        last_updated, pollen_values = render_view()
    resp.html = api.template('index.html', last_updated=last_updated, reload=time.time(), **pollen_values)


@api.route("/api/info")
def api_info(req, resp):
    global last_consume
    global last_updated
    global pollen_values
    # Consume twitter but only if not done within last X minutes
    if last_consume == "" or last_consume < datetime.datetime.now() - datetime.timedelta(minutes=settings.CACHE_TIMER):
        last_consume = datetime.datetime.now()
        check_twitter()
    last_updated, pollen_values = render_view()

    info = {
        "last_updated": last_updated,
        **pollen_values
    }
    resp.media = info


def check_twitter():
    """ Checks for new twitter entries """
    global pollendic
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    access_token = settings.ACCESS_TOKEN
    access_secret = settings.ACCESS_SECRET
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    for status in tweepy.Cursor(api.user_timeline, id='AstmaAllergiDK', tweet_mode='extended').items(5):
        text = status.full_text.lower()
        created = status.created_at
        tweet_id = status.id
        if text.startswith('dagens pollental') or text.startswith('øst:') or text.startswith('vest:'):
            count = 0

            text = text.split(('\n'))
            dataarray = []

            # If øst is not reprecented we go straight to vest.
            if 'øst:' not in text:
                if 'vest:' in text:
                    count = count + 1
            # Lets do some precessing on the tweets
            for line in text:
                if any(x in line for x in pollentypes):
                    if ':' in line:
                        splitline = line.split(':')
                        pollen = splitline[0].strip()
                        value = splitline[1].strip()
                        if value.isdigit():
                            # Simple way of figuring out what location we on
                            if count == 1:
                                location = 'vest'
                            if count == 0:
                                location = 'øst'

                            datalist = {'location': location, 'pollen': pollen, 'value': value}
                            dataarray.append(datalist)
                # If we got trough øst, we can proceed to vest
                if line.startswith('vest:'):
                    count = count + 1

            # Run over each pollen type and update our dictionary
            for item in pollentypes:
                for sublist in dataarray:
                    if sublist['pollen'] == item:
                        ourpollen = {'created': str(created), 
                                     'location': sublist['location'],
                                     'pollen': sublist['pollen'],
                                     'value': sublist['value']
                                    }
                        pollendic.append(ourpollen)
            # Break as soon as we have processed 1 tweet with pollendata
            break


def render_view():
    pollen_values = {}
    # Populate fields with 0 so we are not missing data in our html table.
    for pollen in pollentypes:
        pollen_values[pollen + '_øst'] = 0
        pollen_values[pollen + '_vest'] = 0
    for row in pollendic:
        pollen_values[row['pollen'] + '_' + row['location']] = row['value']
        last_updated = row['created']

    return last_updated, pollen_values


if __name__ == "__main__":
    api.run()
