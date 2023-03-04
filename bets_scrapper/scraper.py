import requests
import json
import re


def scrap_data():

    # Define the URL to scrape
    url = "https://betsniper.vercel.app/"

    try:
        # Make a request to the URL and get the HTML content
        response = requests.get(url)

        # Check if the response was successful
        response.raise_for_status()

        # Regex to extract the JSON data from the HTML content of the page and convert it to a Python dictionary object
        json_data = json.loads(re.findall(
            "<script id=\"__NEXT_DATA__\"[^>]*>(.*?)</script>", response.text, re.DOTALL)[0])

        # Extract the matches data from the JSON data
        matches = json_data["props"]["pageProps"]["matches"]

        return matches
    except requests.exceptions.HTTPError as http_error:
        # Handle HTTP errors
        logging.error(f"HTTP error occurred: {http_error}")
        raise http_error

    except requests.exceptions.RequestException as request_exception:
        # Handle other types of request exceptions
        logging.error(f"Request exception occurred: {request_exception}")
        raise request_exception

    except (ValueError, IndexError, KeyError) as parsing_error:
        # Handle JSON parsing errors
        logging.error(f"JSON parsing error occurred: {parsing_error}")
        raise parsing_error
