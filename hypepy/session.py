import requests

session = requests.Session()
session.headers['User-Agent'] = 'hypepy v0.0.1'  # be nice
session.get('http://hypem.com')


def get(url, **kwargs):
    return session.get(url, **kwargs)
