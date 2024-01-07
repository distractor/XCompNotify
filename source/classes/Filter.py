import logging
import os
from typing import List

import pandas as pd
from classes.Competition import Competition
from helpers.utils import load_old_comps

logger = logging.getLogger(__name__)


class Filter:
    def __init__(self):
        logging.info("Initialize filter class.")
        # Load old comps.
        self.old_comps = load_old_comps()

    def get_new_comps(self, scrapped_comps: List[Competition]):
        logging.info("Searching for new competitions, previously unknown to me.")

        new_comps: List[Competition] = []
        for comp in scrapped_comps:
            if comp not in self.old_comps:
                new_comps.append(comp)

        return new_comps

    def filter_by_duration(self, comps: List[Competition]):
        max_duration = int(os.environ.get("MAX_EVENT_DURATION_DAYS"))
        logging.info("Filtering competitions by duration. Max allowed duration = {}.".format(max_duration))

        new_comps: List[Competition] = []
        for comp in comps:
            if (comp.date_to - comp.date_from).total_seconds() / 86400 < max_duration:
                new_comps.append(comp)

        return new_comps

    def filter_duplicates(self, comps: List[Competition]):
        logging.info("Filtering competitions by duplicates.")

        # Map to pandas dataframe.
        data = pd.DataFrame(comps)
        # Map names to lower case.
        data['name'] = data['name'].str.lower()
        # Find duplicated items by name and dates.
        duplicates = data[data.duplicated(subset=['name', 'date_from', 'date_to'])]

        # Decide which duplicate to keep.
        for index, comp1 in duplicates.iterrows():
            comp2 = [c for c in comps if
                     c.name.lower() == comp1['name'] and c.date_from == comp1['date_from'] and c.date_to ==
                     comp1['date_to']][0]
            # Remove.
            remove = comp2 if not comp2.fai_category.isnumeric() else comp1
            comps = [c for c in comps if c != remove]

        return comps
