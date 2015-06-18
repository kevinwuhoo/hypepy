import time
import json
from hypem_urls import *
from hypepy import session
from hypepy.song import Song
from bs4 import BeautifulSoup


class Section(object):

    def __init__(self, page_path, page_limit=3):
        self.page_path = page_path
        self.page_num = 0
        self.page_limit = page_limit

    def __iter__(self):
        return self

    # Python 3
    def __next__(self):
        return self

    def next(self):
        if self.page_num == self.page_limit:
            raise StopIteration()
        else:
            self.page_num += 1
            return self.get_page()

    def get_page(self):
        # Get track data required for downloading song
        url = "{}{}/{}".format(HYPEM_AUTHORITY_URL, self.page_path, self.page_num)
        req = session.get(url, params={'ts': int(time.time())})
        soup = BeautifulSoup(req.text)

        page_track_data = soup.find(id='displayList-data').text
        page_track_data = json.loads(page_track_data)["tracks"]

        tracks = []
        for dom_track, page_track in zip(soup.find_all(class_='section-track'),
                                         page_track_data):

            if dom_track['data-itemid'] != page_track['id']:
                raise('u wot these should be the same')

            id_ = page_track['id']
            title = dom_track.find('a', class_='track')
            artist = dom_track.find('a', class_='artist')
            thumb = dom_track.find('a', class_='thumb')['style']
            ts = page_track['ts']
            key = page_track['key']
            track_url = title['href']

            title = title['title'].split(' - ')[0]
            artist = artist['title'].split(' - ')[0]
            thumb_url = thumb.split('(')[1].split(')')[0]

            tracks.append(Song(id_, title, artist, thumb_url, ts, key, track_url))

        return tracks
