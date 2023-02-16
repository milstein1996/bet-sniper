from gspread.exceptions import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
import pandas as pd
import gspread


class Sheet:
    def __init__(self, sheet_name, worksheet_name):
        self.sheet_name = sheet_name
        self.worksheet_name = worksheet_name
        self.sheet = self.get_sheet()

    def get_sheet(self):
        # use creds to create a client to interact with the Google Drive API
        # Scope: is the level of access you are requesting. Full, readonly, etc.
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "config/credentials.json", scope)
        client = gspread.authorize(creds)

        try:
            spread_sheet = client.open(self.sheet_name)
        except SpreadsheetNotFound:
            # create a new sheet with the given name
            spread_sheet = client.create(self.sheet_name)
            print(
                f"Spreadsheet '{self.sheet_name}' not found. Created a spreadsheet with the same name.")
        except Exception as e:
            print(e)
            print("Something went wrong. Please try again.")
            return None
        return spread_sheet

    def get_worksheet(self, data):
        try:
            # get the worksheet with the given name
            worksheet = self.sheet.worksheet(self.worksheet_name)
        except Exception as e:
            print("Something went wrong. Please try again.")
            raise e
        return worksheet

    def update_sheet(self, data: pd.DataFrame):
        # Get the worksheet
        worksheet = self.get_worksheet(data)

        # Clear the existing data in the sheet
        worksheet.clear()

        # Update the sheet with the new data
        set_with_dataframe(worksheet, data)
