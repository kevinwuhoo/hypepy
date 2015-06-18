import unittest
from hypepy import HypeM
import tempfile
import os


class TestHypeM(unittest.TestCase):

  def test_popular(self):
      popular_pages = list(HypeM.popular())
      first_song = popular_pages[0][0]

      self.assertEqual(len(popular_pages), 3)

      self.assertTrue(len(first_song.artist) > 0)
      self.assertTrue(len(first_song.title) > 0)
      self.assertTrue(first_song.loved_count() > 10)
      self.assertTrue(first_song.repost_count() > 2)

      song_path = first_song.download(tempfile.gettempdir())
      self.assertTrue(os.path.getsize(song_path) > 0)

      first_song_posts = list(first_song.posts())
      self.assertEqual(len(first_song_posts), first_song.repost_count())

if __name__ == '__main__':
    unittest.main()
