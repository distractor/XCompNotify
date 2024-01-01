import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from classes.Notifier import Notifier

path_root = Path(__file__).parent.parent
os.chdir(path_root)

# Initialize logging.
load_dotenv()

notifier = Notifier()
message = ("*Hello pilots!*\nMy admin updated me again. I will now inform you of new competitions from \n"
           "- civlcomps.org,\n- pwca.org and \n- airtribune.com.\n Some events might be duplicated, since events "
           "published on civlcomps are often also published on other pages - life is tough.")
asyncio.run(notifier.send_message(message=message))
