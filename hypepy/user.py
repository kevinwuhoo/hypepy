from .section import Section


class User(object):

    def __init__(self, username):
        self.username = username

    def feed(self):
        return Section("{}/feed".format(self.username), page_limit=None)

    def favorites(self):
        return Section(self.username, page_limit=None)

    def history(self):
        return Section("{}/history".format(self.username), page_limit=None)

    def obsessions(self):
        return Section("{}/obsessed".format(self.username), page_limit=None)
