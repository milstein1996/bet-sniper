from sheet import Sheet
from parse_data import get_parsed_data


def job():
    print("I'm working...")

    # Scrape data
    bets_data = get_parsed_data()

    # create an instance of the Sheet class
    bets_sheet = Sheet("Bets", "Sheet1")

    # update the work sheet with the scraped data
    bets_sheet.update_sheet(bets_data)

    print("I'm done...")


if __name__ == "__main__":
    # Run the Job
    job()
