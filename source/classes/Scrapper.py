import logging
from datetime import datetime

import pycountry
from classes.Competition import Competition
from helpers.scrapping_helper import scrap_civlcomps

logger = logging.getLogger(__name__)


class Scrapper:
    def __init__(self):
        logging.debug("Initialized scrapper.")
        self.obtained_comps = []  # List of all scrapped comps.

    def scrap_all_sources(self):
        logging.info("Scrapping all sources.")

        # Scrap CIVL comps.
        civlcomps = []
        try:
            civlcomps = scrap_civlcomps()
        except RuntimeError as e:
            msg = "Something went wrong while scrapping CIVL page. Error: '{}'.".format(e)
            logging.critical(msg)

        # Convert to dataclasses.
        for comp in civlcomps:
            # Identify country.
            try:
                country = dict(pycountry.countries.lookup(comp['countryIso3']))
            except:
                country['official_name'] = None
            comp_ = Competition(name=comp['eventTitle'],
                                date_from=datetime.strptime(comp['start'], '%Y/%m/%d'),
                                date_to=datetime.strptime(comp['end'], '%Y/%m/%d'),
                                country=country['official_name'] if 'official_name' in country else country['name'],
                                city=comp['cityTitle'],
                                url=comp['eventLink']
                                )
            self.obtained_comps.append(comp_)

        # # Scrap PWCA.
        # pwca_comps = []
        # try:
        #     pwca_comps = scrap_pwca()
        # except RuntimeError as e:
        #     msg = "Something went wrong while scrapping PWCA page. Error: '{}'.".format(e)
        #     logging.critical(msg)
        #
        # for comp in pwca_comps:
        #     comp_name = comp['name']
        #     try:
        #         comp_city = comp["location"][1]["name"]
        #     except:
        #         comp_city = None
        #
        #     comp_ = Competition(name=comp_name,
        #                         date_from=datetime.strptime(comp['startDate'], '%Y-%m-%d'),
        #                         date_to=datetime.strptime(comp['endDate'], '%Y-%m-%d'),
        #                         country=None,
        #                         city=comp_city,
        #                         url=comp['url']
        #                         )
        #     self.obtained_comps.append(comp_)
        #
        # # Scrap AIRTRIBUNE.
        # airtribune_comps = []
        # try:
        #     airtribune_comps = scrap_airtribune()
        # except RuntimeError as e:
        #     msg = "Something went wrong while scrapping AIRTRIBUNE page. Error: '{}'.".format(e)
        #     logging.critical(msg)
        #
        # for comp in airtribune_comps:
        #     comp_ = Competition(name=comp['title'],
        #                         date_from=datetime.strptime(comp['start_date'], '%Y-%m-%d'),
        #                         date_to=datetime.strptime(comp['end_date'], '%Y-%m-%d'),
        #                         country=comp['country']['name'],
        #                         city=comp['place'],
        #                         url="https://airtribune.com{}".format(comp['url'])
        #                         )
        #     self.obtained_comps.append(comp_)
