# pollen
Danish pollen stats

This was built for a free account on herokuapp.com

There is some caching going on and simple javascript to query twitter dynamically on load. 
This assures we get updated numbers after pageload if its not the latest.

Dynaconf env variables:
```
DYNACONF_ACCESS_SECRET=
DYNACONF_ACCESS_TOKEN=
DYNACONF_CONSUMER_KEY=
DYNACONF_CONSUMER_SECRET=
DYNACONF_CACHE_TIMER=300
```