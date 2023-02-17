from gspread.exceptions import SpreadsheetNotFound
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
import pandas as pd
import gspread
import os


class Sheet:
    def __init__(self, sheet_name, worksheet_name):
        self.sheet_name = sheet_name
        self.worksheet_name = worksheet_name
        self.sheet = self.get_sheet()

    def get_sheet(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        # Get the GCP_SERVICE_ACCOUNT_INFO from the environment variable
        GCP_SERVICE_ACCOUNT_INFO = os.environ.get('GCP_SERVICE_ACCOUNT')

        # If the environment variable is not set, return None
        if GCP_SERVICE_ACCOUNT_INFO is None:
            print("GCP_SERVICE_ACCOUNT is not set")
            raise Exception("GCP_SERVICE_ACCOUNT is not set")

        #
        creds = Credentials.from_service_account_info(
            GCP_SERVICE_ACCOUNT_INFO, scopes=scope)

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

        try:
            # Get the worksheet
            worksheet = self.get_worksheet(data)

            # Clear the existing data in the sheet
            worksheet.clear()

            # Update the sheet with the new data
            set_with_dataframe(worksheet, data)
        except Exception as e:
            print("Something went wrong. Please try again.")
            raise e
