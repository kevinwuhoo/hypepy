class Blog(object):
    def __init__(self, id_, name, url, external_post_url):
        self.id_ = id_
        self.name = name
        self.url = url
        self.external_post_url = external_post_url

    def __str__(self):
        return self.name
