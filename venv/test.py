from scheduling.Asset import Asset
from scheduling.Trip import Trip
from scheduling.Journey import Journey
from scheduling.Location import Location

import datetime as dt

locations = [Location("Sydney", (0,0)), Location("Brisbane", (1,1))]

names = [x.latlong for x in locations]

print(names)

# test = Asset(name="eli 747", owner="eli airways")
# trip1 = Trip(test, dt.datetime(2022,1,10,12), dt.datetime(2022,1,10,12,31), locations[0], locations[1])

# print(trip1.duration())