import pandas as pd
from scraper import scrap_data
import datetime


def get_data():
    matches = scrap_data()
    data = [{"Bookmaker": odd["bookmaker"],
             "Match": match["match"],
             "Player": player["player"],
             "Bet": f'{bet["type"]} {odd["line"]}',
             "Type": bet["type"],
             "Line": odd["line"],
             "Over odds": odd["outcomes"]["over"],
             "Under odds": odd["outcomes"]["under"],
             "Scrape time": datetime.datetime.now().strftime("%H:%M:%S")
             }
            for match in matches
            for player in match["players"]["players"]
            for bet in player["bets"]
            for odd in bet["odds"]
            ]
    return data


def get_parsed_data():
    data = get_data()
    df = pd.DataFrame(data)
    return df


get_parsed_data()
