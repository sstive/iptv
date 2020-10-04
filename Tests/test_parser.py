import unittest
from Utils import parser


class ParserTest(unittest.TestCase):

    def test_normal(self):
        channels = parser.load('https://raw.githubusercontent.com/sstive/iptv/master/Tests/playlists/test_1.m3u8')
        print(channels)
        self.assertListEqual(
            [
                {'title': ' Channel 1', 'uri': 'http://url1.test/ch1', 'group_title': 'Group 1'},
                {'title': ' Channel 2', 'uri': 'http://url1.test/ch1', 'group_title': 'Group 2'},
                {'title': ' Channel 3', 'uri': 'http://url1.test/ch3', 'group_title': ''},
                {'title': ' Channel 4', 'uri': 'http://url1.test/ch4', 'group_title': 'Group 4'}
            ],
            channels
        )

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

    def test_empty_m3u(self):
        channels = parser.load('https://raw.githubusercontent.com/sstive/iptv/master/Tests/playlists/test_1.m3u8')
