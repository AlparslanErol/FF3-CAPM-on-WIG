from data_scraper.selenium.selenium_scraper import SeleniumScraper
import argparse


def main(args=None):
    selenium_scraper = SeleniumScraper()
    selenium_scraper.wig_market_data_scraper() if args.scrape_type == "wig" else selenium_scraper.company_stock_scraper()


if __name__ == "__main__":
    """
    Create arg parser to parse arguments from the terminal to decide the type of scraper if it will be 
    a "company" type scraper or a "wig" type scraper.
    """
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument(
        "-s",
        "--scrape-type",
        type=str,
        required=False,
        default="wig",
        help="Please select scraper type: company or wig",
    )
    args = my_parser.parse_args()
    main(args=args)
