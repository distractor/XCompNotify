import dataclasses
import json
import logging
import os
from datetime import datetime

import pycountry

from classes.Competition import Competition


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def assemble_new_competition_message(comp: Competition):
    msg = "*New event published:*\n"
    msg += "[{}]({})\n".format(comp.name, comp.url)
    msg += "From: {}\n".format(comp.date_from.strftime('%d %B %Y'))
    msg += "To: {}\n".format(comp.date_to.strftime('%d %B %Y'))
    if comp.country is not None:
        try:
            country = dict(pycountry.countries.lookup(comp.country))
            msg += "Location: {}, {}\n".format(country['name'], comp.city)
        except:
            msg += "Location: {}\n".format(comp.city)

    return msg


# Load old comps.
def load_old_comps():
    file_path = "data/old_comps.json"
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
                            url=comp['url']
                            )
        result.append(comp_)
    return result


def save_comps_to_json(comps):
    file_path = "data/old_comps.json"
    logging.debug("Saving all competitions to '{}'.".format(file_path))

    if os.path.exists(file_path):
        # If history exists, append new comps.
        old_comps = load_old_comps()
        comps = old_comps + comps
    with open(file_path, 'w') as file:
        json.dump(comps, file, cls=EnhancedJSONEncoder, indent=2)
