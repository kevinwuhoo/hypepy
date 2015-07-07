from .section import Section

from .hypem_urls import *
from hypepy import session
from bs4 import BeautifulSoup

class User(object):

    def __init__(self, username):
        self.username = username

        self.url = HYPEM_USER_URL.format(username)
        self._friends = None

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
                self._friends.append(User(username))

            page_num += 1

        return self._friends
