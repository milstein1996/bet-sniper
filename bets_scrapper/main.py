from sheet import Sheet
from parse_data import get_parsed_data
import logging


def job():
    try:
        logging.info("I'm working...")

        # Scrape data
        bets_data = get_parsed_data()

        # create an instance of the Sheet class
        # If sheet_name, and worksheet_name change; update Bet Scrape, and Sheet1 with the respective names
        bets_sheet = Sheet(sheet_name="Bet Scrape", worksheet_name="Sheet1")

        # update the work sheet with the scraped data
        bets_sheet.update_sheet(bets_data)

        logging.info("I'm done...")
    except Exception as error:
        logging.error(f"Error occurred while updating sheet: {error}")
        raise e


if __name__ == "__main__":
    # Run the Job
    job()
