# Class for storing truck data into truck object
class TruckData:
    def __init__(self, packages, address, miles, max_load, depart_time):
        self.packages = packages
        self.address = address
        self.miles = miles
        self.max_load = max_load
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.packages, self.address, self.miles, self.max_load, self.depart_time)
