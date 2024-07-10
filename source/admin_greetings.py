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
message = (
    "*Hello pilots!*\nMy admin updated me again. I was extremely annoying. So I will now update you only about "
    "competitions from Italy, Slovenia, Croatia, Austria and Germany. Also check [https://adrenalinco.si/tekme/]("
    "https://adrenalinco.si/tekme/), where a list and calendar views of all competitions are automatically generated.")
asyncio.run(notifier.send_message(message=message))
