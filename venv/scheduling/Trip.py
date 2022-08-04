from Asset import Asset
from Location import Location
from datetime import datetime, timedelta

class Trip:
    def __init__(self, asset: Asset, 
                date_from: datetime, date_to: datetime, 
                loc_from: Location, loc_to: Location) -> None:
                    self.asset = asset
                    self.date_from = date_from
                    self.date_to = date_to

    def duration(self):
        """Returns the duration of the trip in hours """
        return timedelta((self.date_to - self.date_from).hours)


"""
Use composition rather than inheritance

E.g., Flight has a Trip as overall trip to final destination (Departure to Arrival)
Within the Trip, you have a list of Flights

Trip: Departure to Arrival
Flight: list of movements within the trip (loc_from to loc_to)

E.g., Trip.Flight[0].duration()


Journey has multiple...
Trip which has multiple...
Personnel


"""