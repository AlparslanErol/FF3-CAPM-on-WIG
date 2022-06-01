from unittest import TestCase

import pandas as pd
import selenium

from data_scraper.utils.utils import get_wig_list, get_chrome_driver


class TestUtils(TestCase):
    def test_get_wig_list(self):
        test_out = get_wig_list()
        self.assertIsInstance(test_out, pd.DataFrame)
        self.assertEqual(test_out.shape, (342, 9))
        self.assertEqual(test_out.columns[0], 'Nazwa')
        self.assertEqual(test_out.columns[-2], 'Pakiet')

    def test_get_chrome_driver(self):
        test_driver = get_chrome_driver()
        self.assertIsInstance(test_driver, selenium.webdriver.chrome.webdriver.WebDriver)
        self.assertEqual(test_driver.name, "chrome")
