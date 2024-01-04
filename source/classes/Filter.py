import logging
import os
from typing import List

from helpers.utils import load_old_comps

from source.classes.Competition import Competition

logger = logging.getLogger(__name__)


class Filter:
    def __init__(self):
        logging.info("Initialize filter class.")
        # Load old comps.
        self.old_comps = load_old_comps()

    def get_new_comps(self, scrapped_comps: List[Competition]):
        logging.info("Searching for new competitions, previously unknown to me.")

        new_comps = []
        for comp in scrapped_comps:
            if comp not in self.old_comps:
                new_comps.append(comp)

        return new_comps

    def filter_by_duration(self, comps: List[Competition]):
        max_duration = int(os.environ.get("MAX_EVENT_DURATION_DAYS"))
        logging.info("Filtering competitions by duration. Max allowed duration = {}.".format(max_duration))

        new_comps = []
        for comp in comps:
            if (comp.date_to - comp.date_from).total_seconds() / 86400 < max_duration:
                new_comps.append(comp)

        return new_comps
