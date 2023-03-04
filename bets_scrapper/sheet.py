from gspread.exceptions import SpreadsheetNotFound
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
import pandas as pd
import gspread
import os
import json
import logging


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
            logging.error("GCP_SERVICE_ACCOUNT is not set")
            return None

        #
        creds = Credentials.from_service_account_info(
            json.loads(GCP_SERVICE_ACCOUNT_INFO), scopes=scope)

        client = gspread.authorize(creds)

        try:
            spread_sheet = client.open(self.sheet_name)
        except SpreadsheetNotFound:
            logging.error(
                f"Spreadsheet '{self.sheet_name}' not found!")
            raise None

        except Exception as error:
            logging.error(f"Something went wrong. Please try again: {error}")
            return None

        return spread_sheet

    def get_worksheet(self, data):
        try:
            # get the worksheet with the given name
            worksheet = self.sheet.worksheet(self.worksheet_name)
        except Exception as error:
            logging.error(f"Something went wrong. Please try again: {error}")
            return None
        return worksheet

    def update_sheet(self, data: pd.DataFrame):

        try:
            # Get the worksheet
            worksheet = self.get_worksheet(data)

            # Clear the existing data in the sheet
            worksheet.clear()

            # Update the sheet with the new data
            set_with_dataframe(worksheet, data)
        except Exception as error:
            logging.error("Something went wrong. Please try again: {error}")
            raise error
