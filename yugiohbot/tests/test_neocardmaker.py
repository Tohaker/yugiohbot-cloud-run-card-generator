import os
import sys
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from card import neocardmaker


class TestNeoCardMaker(unittest.TestCase):
    def setUp(self):
        if sys.platform == 'linux':
            os.environ['CHROMIUM'] = '/home/travis/bin/chromium-browser'
            os.environ['CHROMEDRIVER'] = '/home/travis/bin/chromedriver'
        else:
            os.environ['CHROMIUM'] = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            os.environ['CHROMEDRIVER'] = 'C:\\Program Files\\chromedriver\\chromedriver.exe'

        url = 'https://yemachu.github.io/cardmaker/'
        self.test_driver = neocardmaker.setup_web_driver(url)
        self.test_driver.implicitly_wait(1)

    def test_get_web_driver(self):
        driver = neocardmaker.get_chrome_web_driver()
        self.assertEqual(driver.name, 'chrome')

    def test_setup_web_driver(self):
        self.assertTrue("Neo New card maker" in self.test_driver.title)

    def test_start_new_card(self):
        neocardmaker.start_new_card(self.test_driver)
        name = self.test_driver.find_element(By.XPATH, '//label[text()=\"Name\"]/input[1]')
        self.assertEqual(name.text, '')

    def test_fill_text_box(self):
        expected = '123'
        test_names = ['Name', 'Level', 'Image', 'Type', 'Attack',
                      'Defense and/or Link', 'Set id', 'Serial number', 'Copyright']
        for name in test_names:
            neocardmaker.fill_text_box(self.test_driver, name, expected)
            text_box = self.test_driver.find_element(By.XPATH, '//label[text()=\"' + name + '\"]/input[1]')
            actual = text_box.get_attribute('value')
            self.assertTrue(expected in actual)

    def test_fill_text_area(self):
        expected = 'this is\na multiline\nentry'
        neocardmaker.fill_text_area(self.test_driver, 'Effect', expected)
        text_area = self.test_driver.find_element(By.XPATH, '//label[text()=\"Effect\"]/textarea[1]')
        actual = text_area.get_attribute('value')
        self.assertTrue(expected in actual)

    def test_select_from_drop_down(self):
        rarity_options = ['common', 'rare', 'ultra', 'secret']
        expected = ['Common', 'Rare', 'Ultra rare', 'Secret rare']
        for i, option in enumerate(rarity_options):
            neocardmaker.select_from_drop_down(self.test_driver, 'Rarity', option)
            drop_down = Select(self.test_driver.find_element(By.XPATH, '//label[text()=\"Rarity\"]/select[1]'))
            selected = drop_down.first_selected_option.text
            self.assertEqual(selected, expected[i])

    def test_download_card_image(self):
        path = 'test_card.png'
        neocardmaker.download_card_image(self.test_driver, path)
        self.assertTrue(os.path.isfile(path))
        os.remove(path)


if __name__ == '__main__':
    unittest.main()
