import unittest
from Utils import parser


class ParserTest(unittest.TestCase):

    def test_normal(self):
        channels = parser.load('https://raw.githubusercontent.com/sstive/iptv/master/Tests/playlists/test_normal.m3u8')
        self.assertListEqual(
            [
                {'title': 'Channel 1', 'uri': 'http://url1.test/ch1', 'group_title': 'Group 1'},
                {'title': 'Channel 2', 'uri': 'http://url1.test/ch2', 'group_title': 'Group 2'},
                {'title': 'Channel 3', 'uri': 'http://url1.test/ch3', 'group_title': ''},
                {'title': 'Channel 4', 'uri': 'http://url1.test/ch4', 'group_title': 'Group 4'}
            ],
            channels
        )

    def test_bad_url(self):
        channels = parser.load('bad_url')
        self.assertIsNone(channels)

    def test_url_not_found(self):
        channels = parser.load('http://www.hhjhjhakjjashjkjhkasfjhakfjh.asd/not_found')
        self.assertIsNone(channels)

    def test_not_m3u(self):
        channels = parser.load('https://www.github.com/')
        self.assertIsNone(channels)

    def test_empty_m3u(self):
        channels = parser.load('https://raw.githubusercontent.com/sstive/iptv/master/Tests/playlists/test_empty.m3u8')
        self.assertListEqual([], channels)

    def test_real(self):
        channels = parser.load('https://iptvmaster.ru/russia.m3u')
        print(channels)
