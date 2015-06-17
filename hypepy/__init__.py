from .section import Section
import datetime


class HypeM(object):

    # Popular Tab
    @staticmethod
    def popular():
        return Section('popular')

    @staticmethod
    def lastweek():
        return Section('lastweek')

    @staticmethod
    def time_machine(year, month, day):
        inputted_date = datetime.date(year, month, day)

        # first week of time machine
        if inputted_date < datetime.date(2007, 10, 22) or \
           inputted_date > datetime.datetime.now().date():
            raise Exception('Date must be between 2007-10-22 and today.')

        # Date format in url is Mar-08-2010
        return Section("popular/week:{:%b-%d-%Y}".format(inputted_date))

    @staticmethod
    def popular_remix():
        return Section('popular/remix')

    @staticmethod
    def popular_noremix():
        return Section('popular/noremix')

    @staticmethod
    def popular_artist():
        return Section('popular/artist', page_limit=1)

    @staticmethod
    def twitter():
        return Section('twitter/popular', page_limit=5)
