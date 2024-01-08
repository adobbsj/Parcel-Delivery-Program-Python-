# Class for storing Package data into Package object.
class Package:
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.Deadline_time, self.weight, self.delivery_time,
                                                       self.status)

    # Custom method for setting the delivery status of a package based on the time
    def packageStatus(self, timeConversion):
        if self.delivery_time < timeConversion:
            self.status = "Delivered"
        elif self.departure_time < timeConversion:
            self.status = "En route"
        else:
            self.status = "in Hub"

    # custom method for updating package 9 at 10:20 AM
    def update(self, address, zipcode):
        self.address = address
        self.zipcode = zipcode
