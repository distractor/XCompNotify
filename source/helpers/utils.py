import dataclasses
import json
import logging
import os
from datetime import datetime
from typing import List

import requests
from classes.Competition import Competition


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def assemble_new_competition_message_list(comps: List[Competition]):
    msg = "*New events published:*\n"
    for comp in comps:
        msg += "- [{}]({}), {}\n".format(comp.name, comp.url, comp.country)
    msg += "\nCheck [adrenalinco](https://adrenalinco.si/tekme/) for complete calendar and list views."

    return msg


def assemble_new_competition_message(comp: Competition):
    msg = "*New event published:*\n"
    msg += "[{}]({})\n".format(comp.name, comp.url)
    msg += "From: {}\n".format(comp.date_from.strftime('%d %B %Y'))
    msg += "To: {}\n".format(comp.date_to.strftime('%d %B %Y'))
    msg += "Location: {}, {}\n".format(comp.country, comp.city)
    msg += "FAI category: {}\n".format(comp.fai_category)
    msg += "\nCheck [adrenalinco](https://adrenalinco.si/tekme/) for complete calendar and list views."

    return msg


# Load old comps.
def load_old_comps():
    file_path = "data/comps.json"
    logging.info("Loading competitions already known to me from '{}'.".format(file_path))
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except:
        data = {}

    # Convert to internal dataclasses.
    result = []
    for comp in data:
        comp_ = Competition(name=comp['name'],
                            date_from=datetime.fromisoformat(comp['date_from']),
                            date_to=datetime.fromisoformat(comp['date_to']),
                            country=comp['country'],
                            city=comp['city'],
                            url=comp['url'],
                            fai_category=comp['fai_category']
                            )
        result.append(comp_)
    return result


def save_comps_to_json(comps):
    file_path = "data/comps.json"
    logging.debug("Saving all competitions to '{}'.".format(file_path))

    if os.path.exists(file_path):
        # If history exists, append new comps.
        old_comps = load_old_comps()
        comps = old_comps + comps
    with open(file_path, 'w') as file:
        json.dump(comps, file, cls=EnhancedJSONEncoder, indent=2)


def post_json_to_adrenalinco():
    logging.info("Posting JSON to Adrenalinco ...")
    file_path = "data/comps.json"
    url = os.environ.get('URL_ADRENALINCO')
    payload = {}
    files = [
        ('jsonFile', (
            'comps.json', open(file_path, 'rb'),
            'application/octet-stream'))
    ]
    headers = {
        'Cookie': 'PH_HPXY_CHECK=s1'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        logging.info(response.text)
    except requests.exceptions.ConnectionError as e:
        logging.error("Something went wrong while posting competitions to ADRENALINCO. Error: {}".format(e))
