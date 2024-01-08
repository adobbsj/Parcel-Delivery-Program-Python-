# Author: Armondo Dobbs Jr
# Student ID: 010111115
# Title: C950 WGU ROUTING PROGRAM PERFORMANCE ASSESSMENT

# import calls to connect the other classes to main.py
import csv
import datetime
import Truck
from Package import Package
from HashMap import CreateHashMap

# this initializes all the distance information to be used in the calculateDistance function.
with open("csv_items/distanceInfo.csv") as csvReadDistance:
    Distance = csv.reader(csvReadDistance, delimiter=",")
    Distance = list(Distance)


# Method which calculates the distance between two locations from the distanceInfo.csv file.
# This operation will always be O(1) as it will only take in a constant two values.
def calculateDistance(col, row):
    distance = Distance[col][row]
    if distance == '':
        distance = Distance[row][col]
    return float(distance)


# this initializes all the address information to be used in the getAddress function.
with open("csv_items/addressInfo.csv") as csvReadAddress:
    Address = csv.reader(csvReadAddress, delimiter=",")
    Address = list(Address)


# Method which gets a particular address from the addressInfo.csv file for each truck to use.
# This operation will always be O(n) as it will iterate through the entire list every time it is called.
def getAddress(address):
    for row in Address:
        if address in row[2]:
            return int(row[0])


# this initializes all the package information to be used in the startData function.
with open("csv_items/packageInfo.csv") as csvReadPackage:
    Package1 = csv.reader(csvReadPackage, delimiter=",")
    Package1 = list(Package1)


# Method which initializes all the package information from the packageInfo.csv and stores it into the hashtable.
# This operation will always be O(n) as it will iterate through the entire file every time it is called.
def startData(file, hashMap):
    with open(file) as packageData:
        package_data = csv.reader(packageData)
        for package in package_data:
            ID = int(package[0])
            address = package[1]
            City = package[2]
            State = package[3]
            Zipcode = package[4]
            Deadline_time = package[5]
            Weight = package[6]
            Status = "in Hub"

            # Here, the package data is turned into a package object and then stored in the hash table.
            newPackage = Package(ID, address, City, State, Zipcode, Deadline_time, Weight, Status)
            hashMap.insert(ID, newPackage)


# initializing the hashmap to then call the startData function and begin the package allocation process.
hashMapPackage = CreateHashMap()
package_insert = "csv_items/packageInfo.csv"
startData(package_insert, hashMapPackage)

# Manually loading the packages into the trucks with the starting location being WGU.
# If this project were to be changed, automatically loading and unloading trucks would be implemented.
firstTruck = Truck.TruckData([1, 13, 14, 15, 16, 19, 20, 23, 29, 30, 31, 34, 37, 39, 40], "4001 South 700 East", 0.0, 16,
                             datetime.timedelta(hours=8))

secondTruck = Truck.TruckData([2, 3, 4, 5, 6, 12, 18, 25, 26, 27, 28, 32, 36, 38], "4001 South 700 East",
                              0.0, 16, datetime.timedelta(hours=9, minutes=5))

thirdTruck = Truck.TruckData([7, 8, 9, 10, 11, 17, 21, 22, 24, 33, 35], "4001 South 700 East", 0.0, 16,
                             datetime.timedelta(hours=10, minutes=20))


# This is the primary method for calculating the shortest path using the nearest neighbor algorithm. A delivery array
# is created and a loop iterates where if the distance to the current location in the queue is shorter than the
# distance to the next, then set the current queued to the next destination.
# This operation will always be O(n^2) as it will iterate through every package in the trucks while also iterating
# through the packages that still need delivering.
def deliveryRoute(truck):
    # Initializing a new array for every package in the trucks that still need to be delivered. Once created,
    # the old list will be cleared out because we will sort the new array with the nearest neighbor algorithm and
    # then put them back in the truck.
    needsDelivery = []
    for ID in truck.packages:
        package = hashMapPackage.search(ID)
        needsDelivery.append(package)

    truck.packages.clear()

    # This section sorts the packages by distance and will put the shorter length of two packages back into the truck.
    # The package with the longer length will then be compared to the next package in the array and repeated.
    while len(needsDelivery) > 0:
        newAddress = 1000
        newPackage = None
        for package in needsDelivery:
            if calculateDistance(getAddress(truck.address), getAddress(package.address)) <= newAddress:
                newAddress = calculateDistance(getAddress(truck.address), getAddress(package.address))
                newPackage = package

        # Here is where all the truck information is updated once a package has been placed back into it and delivered.
        truck.packages.append(newPackage.ID)
        needsDelivery.remove(newPackage)
        truck.miles += newAddress
        truck.address = newPackage.address
        truck.time += datetime.timedelta(hours=newAddress / 18)  # Divide by 18 for the limit of 18 MPH.
        newPackage.delivery_time = truck.time
        newPackage.departure_time = truck.depart_time


# Run the delivery route for every truck
# Add a calculation which makes sure that the third truck does not start until one of the first two trucks finishes.
deliveryRoute(firstTruck)
deliveryRoute(secondTruck)
thirdTruck.depart_time = min(firstTruck.time, secondTruck.time)
deliveryRoute(thirdTruck)


# This is the main class where the user will be able to interact with the program.
# If the user decides they would like to see a single package, the time complexity will be O(1) for a direct search.
# If they would like to see all the packages, the time complexity will be O(n) to generate a list of all packages.
class Main:
    miles = firstTruck.miles + secondTruck.miles + thirdTruck.miles  # The total mileage of the route after finishing.
    print("\nWelcome to Western Governors University Parcel Service")
    print("The total miles for today's delivery route is:", miles)
    print("\nTruck one contains the following packages", firstTruck.packages, "and departs from the hub at:",
          firstTruck.depart_time)
    print("Truck two contains the following packages", secondTruck.packages, "and departs from the hub at:",
          secondTruck.depart_time)
    print("Truck three contains the following packages", thirdTruck.packages, "and departs from the hub at:",
          thirdTruck.depart_time)
    prompt = input("\nType 'start' to begin: ")
    if prompt == "start":
        try:
            time = input("What time would you like to view the status of packages? (format HH:MM:SS): ")
            (h, m, s) = time.split(":")

            # Converting the time input by the user to compare with the trucks current package status
            mainTimeConversion = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            packageNineTime = datetime.timedelta(hours=int(10), minutes=int(20), seconds=int(0))
            packageView = input("Would you like to view a single package 'single' or all packages 'all'?: ")
            if packageView == "single":
                try:
                    packageID = input("Type your package ID: ")
                    # calling the search function of the hash map to find the selected package.
                    # update function implemented to make sure package 9 is delivered to the correct address.
                    if packageID == "9" and mainTimeConversion >= packageNineTime:
                        updateAddress = "410 S State St."
                        updateZipcode = "84111"
                        package = hashMapPackage.search(int(packageID))
                        # manually setting the current status of the package depending on the user time and truck time.
                        package.update(updateAddress, updateZipcode)
                        package.packageStatus(mainTimeConversion)
                        print("\nID:", package.ID, "\nAddress:", package.address, ",", package.city, package.state, ",",
                              package.zipcode, "\nDelivery time:", package.delivery_time,
                              "\nStatus:", package.status)
                    else:
                        package = hashMapPackage.search(int(packageID))
                        # manually setting the current status of the package depending on the user time and truck time.
                        package.packageStatus(mainTimeConversion)
                        print("\nID:", package.ID, "\nAddress", package.address, ",", package.city, package.state, ",",
                              package.zipcode, "\nDelivery time:", package.delivery_time,
                              "\nStatus:", package.status)
                except ValueError:
                    print("Invalid input.")
                    exit()
            elif packageView == "all":
                try:
                    for packageID in range(1, 41):
                        # update function implemented to make sure package 9 is delivered to the correct address.
                        if packageID == 9 and mainTimeConversion >= packageNineTime:
                            updateAddress = "410 S State St."
                            updateZipcode = "84111"
                            # calling the search function of the hash map to find the all packages.
                            package = hashMapPackage.search(int(packageID))
                            # manually setting the current status of the package depending on the user time and truck
                            # time.
                            package.update(updateAddress, updateZipcode)
                            package.packageStatus(mainTimeConversion)
                            print(str(package))
                        else:
                            # calling the search function of the hash map to find the all packages.
                            package = hashMapPackage.search(int(packageID))
                            # manually setting the current status of the package depending on the user time and truck
                            # time.
                            package.packageStatus(mainTimeConversion)
                            print(str(package))
                except ValueError:
                    print("Invalid input.")
                    exit()
            else:
                print("Invalid input.")
                exit()
        except ValueError:
            print("Invalid input.")
            exit()
    elif prompt != "start":
        print("Invalid input.")
        exit()
