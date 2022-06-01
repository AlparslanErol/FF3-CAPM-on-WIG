import typing
from unittest import TestCase

import pandas as pd
from pandas.testing import assert_frame_equal

from data_scraper.selenium.selenium_scraper import SeleniumScraper


class TestSeleniumScraper(TestCase):
    def test_dates_format(self):
        test_scraper = SeleniumScraper()
        self.assertIsInstance(test_scraper, SeleniumScraper)
        test_df = pd.DataFrame.from_dict(
            {
                "mon": ["Dec", "Mar", "Jun", "Sep"],
                "day": ["19", "20", "21", "22"],
                "year": ["2021", "2021", "2021", "2021"],
            }
        )
        self.assertIsInstance(test_df, pd.DataFrame)
        test_out = test_scraper.dates_format(test_df)
        self.assertIsInstance(test_out, pd.DataFrame)
        expected_out = pd.DataFrame.from_dict(
            {"period": ["19-12-2021", "20-03-2021", "21-06-2021", "22-09-2021"]}
        )
        self.assertIsInstance(expected_out, pd.DataFrame)
        assert_frame_equal(test_out, expected_out)
