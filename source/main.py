import asyncio
import logging
import os
from datetime import datetime
from logging import config
from pathlib import Path

from dotenv import load_dotenv

from classes.Filter import Filter
from classes.Notifier import Notifier
from classes.Scrapper import Scrapper
from helpers.utils import assemble_new_competition_message, save_comps_to_json, post_json_to_adrenalinco


def main():
    # Set working directory.
    path_root = Path(__file__).parent.parent
    os.chdir(path_root)

    # Initialize logging.
    config.fileConfig("logging.conf")
    # Take environment variables from .env file
    logging.info("Loading environment variables from '.env'.")
    load_dotenv()

    # Start.
    time_start = datetime.now()
    logging.info("Run started at: {}.".format(time_start))
    logging.info("Working directory - root of the project: {}".format(path_root))

    # Scrap data from web.
    scrapper = Scrapper()
    scrapper.scrap_all_sources()

    # Apply filters to obtained competitions.
    filter = Filter()
    new_comps = filter.filter_duplicates(comps=scrapper.obtained_comps)
    new_comps = filter.filter_by_duration(comps=new_comps)
    new_comps = filter.get_new_comps(scrapped_comps=new_comps)

    # Notify users.
    if len(new_comps) > 0:
        if os.environ.get("SEND_MESSAGES") == "True":
            notifier = Notifier()
            for comp in new_comps:
                message = assemble_new_competition_message(comp=comp)
                asyncio.run(notifier.send_message(message=message))

        # Save new comps to json.
        save_comps_to_json(new_comps)
        # Post new json to adrenalinco.
        post_json_to_adrenalinco()

    else:
        logging.info("No new comps found.")

    # Finalize.
    time_end = datetime.now()
    logging.info("Run finished at: {}.".format(time_end))
    duration = time_end - time_start
    logging.debug("Duration: {}.".format(duration))


if __name__ == "__main__":
    # Run main.
    try:
        main()
    except RuntimeError as e:
        logging.critical("Something went wrong. Error: {}".format(e))
