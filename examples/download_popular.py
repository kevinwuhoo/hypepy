"""
This example script downloads all songs with over 1000 hearts on popular.
"""

from hypepy import HypeM
import os

download_folder = 'popular_songs'
os.makedirs(download_folder, exist_ok=True)

for page in HypeM.popular():

    for song in page:
        msg = '{artist} - {title}, {num_hearts} \u2665...'.format(
                  artist=song.artist,
                  title=song.title,
                  num_hearts=song.loved_count()
              )

        if song.loved_count() > 1000:
            print('Downloading', msg, end='', flush=True)
            result = song.download(download_folder)

            if result:
                print('done.')
            else:
                print('no download link available.')

        else:
            print('Skipping', msg, end='')
            print('skipped.')
