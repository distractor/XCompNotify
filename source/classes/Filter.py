import logging

from helpers.utils import load_old_comps

logger = logging.getLogger(__name__)

class Filter:
    def __init__(self, scrapped_comps):
        logging.info("Initialize filter class.")
        self.scrapped_comps = scrapped_comps
        # Load old comps.
        self.old_comps = load_old_comps()

    def get_new_comps(self):
        logging.info("Searching for new competitions, previously unknown to me.")

        new_comps = []
        for comp in self.scrapped_comps:
            if comp not in self.old_comps:
                new_comps.append(comp)

        return new_comps
