# from Asset import Asset
from scheduling.Location import Location
from datetime import datetime

class Trip:
    def __init__(self, asset: str, 
                date_from: datetime, date_to: datetime, 
                loc_from: Location, loc_to: Location) -> None:
                    self.asset = asset
                    self.date_from = date_from
                    self.date_to = date_to
                    self.loc_from = loc_from
                    self.loc_to = loc_to

    def duration(self):
        """Returns the duration of the trip in minutes"""
        return (self.date_to - self.date_from).seconds/(60)


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