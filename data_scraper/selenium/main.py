from data_scraper.selenium.selenium_scraper import SeleniumScraper


def main(args=None):
    selenium_scraper = SeleniumScraper()
    selenium_scraper.company_stock_scraper()


if __name__ == "__main__":
    main()
