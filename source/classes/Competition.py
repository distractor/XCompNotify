from dataclasses import dataclass
from datetime import datetime


@dataclass
class Competition:
    name: str
    date_from: datetime
    date_to: datetime
    url: str
    country: str
    city: str

    def __init__(self, name, date_from, date_to, country, city, url):
        self.name = name
        self.date_from = date_from
        self.date_to = date_to
        self.country = country
        self.city = city
        self.url = url
