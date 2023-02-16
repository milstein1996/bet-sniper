import requests
import json
import re


def scrap_data():

    # Define the URL to scrape
    url = "https://betsniper.vercel.app/"

    # Make a request to the URL and get the HTML content
    response = requests.get(url)

    # Regex to extract the JSON data from the HTML content of the page and convert it to a Python dictionary object
    json_data = json.loads(re.findall(
        "<script id=\"__NEXT_DATA__\"[^>]*>(.*?)</script>", response.text, re.DOTALL)[0])

    # Extract the matches data from the JSON data
    matches = json_data["props"]["pageProps"]["matches"]

    return matches
