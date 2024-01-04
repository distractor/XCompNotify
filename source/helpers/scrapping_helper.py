import json
import logging
import os

import requests
from bs4 import BeautifulSoup


def scrap_civlcomps():
    url = os.environ.get("URL_CIVLCOMPS")
    payload = {}
    headers = {
        "X-Requested-With": "XMLHttpRequest"
    }

    # Make request.
    logging.debug("Requesting data from CIVL.")
    response = requests.request("GET", url, headers=headers, data=payload)
    logging.debug("Obtained data from CIVL.")
    # Convert to json.
    data = json.loads(response.text)

    if data["loadedCount"] != data["totalCount"]:
        logging.error("Total and loaded comps from CIVL differ! Loaded {} out of {}.".format(data['loadedCount'],
                                                                                             data['totalCount']))
    return data['events']


def scrap_pwca():
    url = os.environ.get("URL_PWCA")
    # Make request.
    logging.debug("Requesting data from PWCA.")
    page = requests.get(url)
    logging.debug("Obtained data from PWCA. Now parsing.")

    # Parse.
    soup = BeautifulSoup(page.content, "html.parser")
    # Obtain div with events.
    results = soup.find(id="evcal_list")
    # Obtain json for each event published.
    events_as_html = results.find_all('script', type='application/ld+json')
    logging.debug("Parsing PWCA completed.")

    # Map to json.
    events = []
    for event in events_as_html:
        events.append(json.loads(event.string))

    return events


def scrap_airtribune():
    url = os.environ.get("URL_AIRTRIBUNE")
    # Make request.
    logging.debug("Requesting data from AIRTRIBUNE.")
    page = requests.get(url)
    logging.debug("Obtained data from AIRTRIBUNE. Now parsing.")

    # Parse.
    soup = BeautifulSoup(page.content, "html.parser")
    # Obtain script with events.
    scripts = soup.find_all('script')
    script = [s.text for s in scripts if "window.ATDATA.eventLists" in s.text][0]
    events = json.loads(script.split(";")[0].split("window.ATDATA.eventLists = ")[-1])
    logging.debug("Parsing AIRTRIBUNE completed.")

    next_events = events['next-events']['content']
    # Keep only XC paragliding events.
    result = [event for event in next_events if event['sport'] == 0]

    return result
