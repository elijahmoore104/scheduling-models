# from Asset import Asset
from turtle import left
from scheduling.Location import Location
from scheduling.Asset import Asset
from datetime import datetime

class Trip:
    """
        There can be multiple Assets on a trip, like a plane w/ a baggage car, or a ship with lineboats and shoreside crew
    """
    def __init__(self, assets: list[Asset], 
                date_from: datetime, date_to: datetime, 
                location_from: Location, location_to: Location) -> None:
                    self.assets = assets
                    self.date_from = date_from
                    self.date_to = date_to
                    self.location_from = location_from
                    self.location_to = location_to
                    self.trip_code = location_from.name[0:3] + "|" + location_to.name[0:3]

    def duration(self):
        """Returns the duration of the trip in minutes"""
        return (self.date_to - self.date_from).seconds/(60)
