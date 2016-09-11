from celery import shared_task
from wander.models import Counter, Trip
import requests


@shared_task
def test_task():
    return "test_task"


@shared_task
def default_task():
    return "default_task"


@shared_task
def change_gps_coordinates():
    count = Counter.objects.get(id=1)

    if count.counter < 16:
        requests.post("https://thingspace.io/dweet/for/arthur",
                      json={"lon": str(count.coordinates['list'][count.counter]['lon']),
                            "lat": str(count.coordinates['list'][count.counter]['lat'])})

        if count.coordinates['list'][count.counter]['fact'] == '1':
            facts = {'list': [{'category': 'History',
                               'title': 'Pier 43',
                               'text': 'Built 1914. Pier 43 and its headhouse, a decorated hoisting tower for loading and unloading rail cars on and off ferries, was built in 1914 to serve the Belt Railroad.',
                               'distance': '0 miles',
                               'lat': '37.809382',
                               'lon': '-122.414465'},
                              {'category': 'Landmark', 'title': 'AT&T Park',
                               'text': 'The park stands along the San Francisco Bay, a segment of which is named McCovey Cove in honor of former Giants player Willie McCovey.',
                               'distance': '0.2 miles',
                               'lat': '37.7786',
                               'lon': '-122.3893'},
                              {'category': 'Restaurants',
                               'title': "Pedro's Cantina",
                               'text': 'Mexican food & margaritas served in a roomy converted warehouse outfitted with many high-def TVs.',
                               'distance': '0.3 miles',
                               'rating': 4,
                               'lat': '37.77935',
                               'lon': '-122.39051'}]
                     }

        if count.coordinates['list'][count.counter]['fact'] == '2':
            facts = {'list': [{'category': 'History',
                               'title': 'Pier 43',
                               'text': 'Built 1914. Pier 43 and its headhouse, a decorated hoisting tower for loading and unloading rail cars on and off ferries, was built in 1914 to serve the Belt Railroad.',
                               'distance': '0 miles',
                               'lat': '37.809382',
                               'lon': '-122.414465'},
                              {'category': 'Landmark', 'title': 'AT&T Park',
                               'text': 'The park stands along the San Francisco Bay, a segment of which is named McCovey Cove in honor of former Giants player Willie McCovey.',
                               'distance': '0.2 miles',
                               'lat': '37.7786',
                               'lon': '-122.3893'},
                              {'category': 'Restaurants',
                               'title': "Pedro's Cantina",
                               'text': 'Mexican food & margaritas served in a roomy converted warehouse outfitted with many high-def TVs.',
                               'distance': '0.3 miles',
                               'rating': 4,
                               'lat': '37.77935',
                               'lon': '-122.39051'}]
                     }

        elif count.coordinates['list'][count.counter]['fact'] == '3':
            facts = {'list': [{'category': 'History',
                               'title': 'Pier 43',
                               'text': 'Built 1914. Pier 43 and its headhouse, a decorated hoisting tower for loading and unloading rail cars on and off ferries, was built in 1914 to serve the Belt Railroad.',
                               'distance': '0 miles',
                               'lat': '37.809382',
                               'lon': '-122.414465'},
                              {'category': 'Landmark', 'title': 'AT&T Park',
                               'text': 'The park stands along the San Francisco Bay, a segment of which is named McCovey Cove in honor of former Giants player Willie McCovey.',
                               'distance': '0.2 miles',
                               'lat': '37.7786',
                               'lon': '-122.3893'},
                              {'category': 'Restaurants',
                               'title': "Pedro's Cantina",
                               'text': 'Mexican food & margaritas served in a roomy converted warehouse outfitted with many high-def TVs.',
                               'distance': '0.3 miles',
                               'rating': 4,
                               'lat': '37.77935',
                               'lon': '-122.39051'}]
                     }
        else:
            facts = {'list': []}

        if Trip.objects.filter(status='live').exists():
            trip = Trip.objects.filter(status='live').latest('id')
            if trip:
                trip.facts = facts
                trip.save()

    if count.counter >= 20:
        count.counter = 0
        count.save()

    count.counter = count.counter + 1
    count.save()
