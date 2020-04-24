import os
import unittest
import random

import app
from utils import gcsutils


class TestApp(unittest.TestCase):

    def setUp(self):
        self.storage_client = gcsutils.create_storage_client(True)

    def test_choose_card_image_spb(self):
        chance = 0.1
        image_destination, card_image_path = app.choose_card_image(self.storage_client, chance)

        self.assertTrue(len(card_image_path) > 0)
        self.assertTrue(len(image_destination) > 0)
        os.remove(card_image_path)

    def test_choose_card_image_cropped(self):
        images = ['1.jpg', '2.jpg']
        chance = 0.5
        image_destination, card_image_path = app.choose_card_image(self.storage_client, chance)

        self.assertTrue(any(i in card_image_path for i in images))
        self.assertTrue(any(i in image_destination for i in images))
        os.remove(card_image_path)

    def test_choose_card_image_submission(self):
        images = ['3.jpg', '4.jpg']
        chance = 0.25
        image_destination, card_image_path = app.choose_card_image(self.storage_client, chance)

        self.assertTrue(any(i in card_image_path for i in images))
        self.assertTrue(any(i in image_destination for i in images))
        os.remove(card_image_path)

    def test_create_card_type(self):
        test_templates = ['Spell', 'Trap', 'Fusion', 'Effect', 'Normal']
        test_race = 'race'
        expected = ['Spell Card', 'Trap Card', 'race / Fusion / Effect', 'race / Effect', 'race']

        for i, t in enumerate(test_templates):
            type = app.create_card_type(t, test_race)
            self.assertEqual(type, expected[i])

    def test_create_card_attribute(self):
        attribute = ['None', 'Dark', 'Divine', 'Earth', 'Fire', 'Light', 'Water', 'Wind']

        a = app.create_card_attribute('Spell')
        self.assertTrue(a == 'Spell')
        a = app.create_card_attribute('Trap')
        self.assertTrue(a == 'Trap')
        a = app.create_card_attribute('Fusion')
        self.assertTrue(any(at in a for at in attribute))

    def test_choose_card_icon(self):
        spell_type = ['None', 'Continuous', 'Counter', 'Equip', 'Field', 'Quick-play', 'Ritual']
        trap_type = ['None', 'Continuous', 'Counter']

        i = app.choose_card_icon('Spell')
        self.assertTrue(any(ic in i for ic in spell_type))
        i = app.choose_card_icon('Trap')
        self.assertTrue(any(ic in i for ic in trap_type))
        i = app.choose_card_icon('Fusion')
        self.assertTrue(i == 'None')

    def test_choose_card_stats(self):
        for level in range(0, 12):
            a, d = app.choose_card_stats(level)
            self.assertTrue(int(a) <= 5000)
            self.assertTrue(int(d) <= 5000)

    def test_get_random_spb_image(self):
        name = app.download_from_shitpostbot()
        self.assertTrue(len(name) > 0)
        os.remove(name)

if __name__ == '__main__':
    unittest.main()
