import datetime
import locale
from .section import Section
from .hypem_urls import *
from hypepy import session
from bs4 import BeautifulSoup

class User(object):

    def __init__(self, username, join_date=None, favorites_count=None,
                 friends_count=None):

        self.username = username

        self.url = HYPEM_USER_URL.format(username)
        self._friends = None

        self._join_date = join_date
        self._favorites_count = favorites_count
        self._friends_count = friends_count

        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

    def feed(self):
        return Section("{}/feed".format(self.username), page_limit=None)

    def favorites(self):
        return Section(self.username, page_limit=None)

    def history(self):
        return Section("{}/history".format(self.username), page_limit=None)

    def obsessions(self):
        return Section("{}/obsessed".format(self.username), page_limit=None)

    def friends(self):
        if self._friends is not None:
            return self._friends
        else:
            self._friends = []

        # friends lists are usually short, I had a hard time finding a user
        # with more than 3 pages of friends, this behavior of scraping all
        # friends then returning should be ok for now
        page_num = 1
        while True:
            req = session.get(HYPEM_FRIENDS_URL.format(self.username, page_num))
            soup = BeautifulSoup(req.text)
            users = soup.find(id='track-list').find_all(class_='user')

            if len(users) == 0:
                break

            for user in users:
                username = user.find('a')['href'].lstrip('/')

                join_date, favorites_count, friends_count = \
                        self._get_join_date_favorites_friends_count_from_soup(user)

                self._friends.append(User(username, join_date,
                                          favorites_count, friends_count))

            page_num += 1

        return self._friends

    def join_date(self):
        self._get_join_date_favorites_friends_count()
        return self._join_date

    def favorites_count(self):
        self._get_join_date_favorites_friends_count()
        return self._favorites_count

    def friends_count(self):
        self._get_join_date_favorites_friends_count()
        return self._friends_count

    def _get_join_date_favorites_friends_count(self):
        if self._join_date is None or self._favorites_count is None or \
           self._friends_count is None:

            req = session.get(self.url)
            soup = BeautifulSoup(req.text)
            self._join_date, self._favorites_count, self._friends_count = \
                    self._get_join_date_favorites_friends_count_from_soup(soup)

    @staticmethod
    def _get_join_date_favorites_friends_count_from_soup(soup):
            # find the join date, parse out the month, day (strip endings),
            # and year and parse the string into a python date
            join_date = soup.find('p', class_='join-date').get_text(strip=True)
            _, month, day, year = join_date.split()
            day = day.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
            day = int(day.rstrip(','))

            join_time = datetime.datetime.strptime("{:02d} {} {}".format(day, month, year), '%d %b %Y')
            join_date = join_time.date()

            favorites_count, friends_count = soup.find_all(class_='big-num')

            favorites_count = locale.atoi(favorites_count.get_text(strip=True))
            friends_count = locale.atoi(friends_count.get_text(strip=True))

            return join_date, favorites_count, friends_count
