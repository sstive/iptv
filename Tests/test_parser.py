import unittest
from Utils import parser


class ParserTest(unittest.TestCase):

    def test_normal(self):
        # TODO: get playlists from raw github
        channels = parser.load('https://iptvmaster.ru/russia.m3u')
        print(channels)
        print(len(channels))

        # TODO: assert dict

    def test_bad_url(self):
        channels = parser.load('bad_url')
        self.assertIsNone(channels)

    def test_url_not_found(self):
        channels = parser.load('http://www.hhjhjhakjjashjkjhkasfjhakfjh.asd/not_found')
        self.assertIsNone(channels)

    def test_not_m3u(self):
        channels = parser.load('https://www.github.com/')
        self.assertIsNone(channels)
