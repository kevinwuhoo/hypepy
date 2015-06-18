import os
import time

from hypem_urls import *
from hypepy import session
from hypepy.blog import Blog
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
from bs4 import BeautifulSoup


class Song(object):
    def __init__(self, id_, title, artist, thumb_url, ts, key, track_url):
        self.id_ = id_
        self.title = title
        self.artist = artist
        self.thumb_url = thumb_url
        self.ts = ts
        self.key = key
        self.track_url = HYPEM_AUTHORITY_URL + track_url.lstrip('/')

        self.thumb_url_medium = os.path.splitext(thumb_url)[0] + '_120.jpg'
        self.thumb_url_large = os.path.splitext(thumb_url)[0] + '_320.jpg'

        # These attribute are private because the data is actually lazily
        # loaded (scraped). The respective functions determines if scraping
        # needs to occur, or the data just needs to be returned.
        self._download_url = None
        self._mp3 = None
        self._loved_count = None
        self._repost_count = None
        self._posts = None

    def download_url(self):
        if not self._download_url:
            # get the actual url to the song by requesting json data with song info
            req = session.get(HYPEM_SERVE_URL.format(self.id_, self.key),
                              headers={'Content-Type': 'application/json'})

            if req.ok:
                self._download_url = req.json()['url']
            else:
                self._download_url = None

        return self._download_url

    def download(self, path):

        filename = '{}/{} - {}.mp3'.format(path, self.artist, self.title)

        if not self._mp3:
            self._mp3 = session.get(self.download_url()).content

        open(filename, 'w').write(self._mp3)

        # TODO maybe do this manipulation in memory since song is stored
        cover_img = session.get(self.thumb_url_large).content
        audio = MP3(filename, ID3=ID3)
        audio.add_tags()

        audio['TIT2'] = TIT2(encoding=3, text=unicode(self.title))
        audio['TPE1'] = TPE1(encoding=3, text=unicode(self.artist))

        audio.tags.add(
            APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=cover_img
            )
        )
        audio.save()

        return filename

    def repost_count(self):
        self._get_loved_repost_count()
        return self._repost_count

    def loved_count(self):
        self._get_loved_repost_count()
        return self._loved_count

    def posts(self):
        if self._posts is None:
            req = session.get(HYPEM_POSTS_URL.format(self.id_, int(time.time())))
            soup = BeautifulSoup(req.text)

            self._posts = []
            for post in soup.find_all('p', class_='more-excerpts'):
                blog = post.find('a', class_='blog-fav-off')

                name = blog.get_text(strip=True)
                url = HYPEM_AUTHORITY_URL + blog['href'].lstrip('/')
                id_ = url.split('/')[-1]
                external_post_url = post.find('a', class_='readpost')['href']

                self._posts.append(Blog(id_, name, url, external_post_url))

        return self._posts

    def _get_loved_repost_count(self):
        if not self._loved_count or not self._repost_count:
            req = session.get(self.track_url)
            soup = BeautifulSoup(req.text)

            loved_count = soup.find('a', class_='toggle-favorites')['title']
            loved_count = loved_count.lstrip('Favorited by ').rstrip(' others')
            self._loved_count = int(loved_count)

            repost_count = soup.find('a', class_='toggle-reposts')
            # if there isn't more than one post about this song, this dom
            # element doesnt exist -- i think
            if repost_count:
                repost_count = repost_count.get_text(strip=True)
                repost_count = repost_count.lstrip('Posted by ').rstrip(' blogs')
            else:
                repost_count = 1

            self._repost_count = int(repost_count)

    def __str__(self):
        return "%s - %s" % (self.title, self.artist)
