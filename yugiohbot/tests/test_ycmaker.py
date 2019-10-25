import unittest
import os
from card import ycmaker


class TestYugiohCardMaker(unittest.TestCase):
    def test_construct_request_valid_args(self):
        expected = 'https://www.yugiohcardmaker.net/ycmaker/createcard.php?name=&cardtype=Monster&trapmagictype=Quick-Play&subtype=normal&attribute=Light&level=1' \
                   '&rarity=Common&picture=&circulation=&set1=&set2=&type=&carddescription=&atk=&def=&creator=&year=2019&serial='
        result = ycmaker.construct_request(cardtype='Monster', trapmagictype='Quick-Play', subtype='normal',
                                           attribute='Light', level=1,
                                           rarity='Common', year=2019)
        self.assertEqual(expected, result)

    def test_construct_request_no_args(self):
        expected = 'https://www.yugiohcardmaker.net/ycmaker/createcard.php?name=&cardtype=&trapmagictype=&subtype=&attribute=&level=' \
                   '&rarity=&picture=&circulation=&set1=&set2=&type=&carddescription=&atk=&def=&creator=&year=&serial='
        result = ycmaker.construct_request()
        self.assertEqual(expected, result)

    def test_download_image_valid_url(self):
        url = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
        path = 'test-image.png'
        ycmaker.download_image(url, path)
        self.assertTrue(os.path.isfile(path))
        os.remove(path)

    def test_download_image_invalid_url(self):
        url = ''
        path = 'test-image.png'
        ycmaker.download_image(url, path)
        self.assertFalse(os.path.isfile(path))

if __name__ == '__main__':
    unittest.main()
