from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hypepy',
    version='0.0.1',
    description='Hypepy is a wrapper and extension of the Hype Machine API.',
    long_description=long_description,
    url='https://github.com/kevinwuhoo/hypepy',

    author='Kevin Wu',
    author_email='me@kevinformatics.com',

    packages=['hypepy'],
    install_requires=['requests', 'BeautifulSoup4', 'mutagen'],
    test_suite="tests",

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
