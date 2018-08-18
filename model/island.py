import logging
import csv


class Island():
    def __init__(self, name :str):
        self.name = name
        self.map = None

class IslandLocation():

    NORMAL = "normal"
    FLOODED = "flooded"
    SUNK = "sunk"


    def __init__(self, name : str, start : str, temple : str, is_exit : str):
        self.name = name
        self.start = start
        self.temple = temple
        self._state =  IslandLocation.NORMAL

        if start == "":
            self.start = None

        if temple == "":
            self.temple = None

        if is_exit == "":
            self.is_exit = False
        else:
            self.is_exit = True

    def __str__(self):
        str = self.name

        if self.start is not None:
            str += ", starting location for {0}".format(self.start)

        if self.temple is not None:
            str += ", Temple for {0} treasure".format(self.temple)

        if self.is_exit is True:
            str += ", exit from the game"

        return str

    def water_rise(self):

        if self._state == IslandLocation.NORMAL:
            self._state = IslandLocation.FLOODED
        elif self._state == IslandLocation.FLOODED:
            self._state = IslandLocation.SUNK

        return self._state


class IslandLocationFactory():

    def __init__(self):
        self.locations = {}

    def load(self, data_dir : str, data_file_name : str):

        file_location = "{0}\\{1}".format(data_dir, data_file_name)

        logging.debug("Loading locations from {0}".format(file_location))

        # Attempt to open the file
        with open(file_location, 'r') as object_file:

            # Load all rows in as a dictionary
            reader = csv.DictReader(object_file)

            # Get the list of column headers
            header = reader.fieldnames

            # For each row in the file....
            for row in reader:
                print(str(row))
                name = row.get("Name")
                start = row.get("Start")
                temple = row.get("Temple")
                is_exit = row.get("Exit")

                new_location = IslandLocation(name, start, temple, is_exit)

                self.locations[name] = new_location

            # Close the file
            object_file.close()

            logging.debug("Finished loading {0} locations.".format(len(self.locations.keys())))


    def print(self):
        for location in self.locations.values():
            print(str(location))

class IslandMap():
    def __init__(self, name: str):
        self.name = name
        self.layout = []
        self.squares = []

        #logging.debug("Constructing new map {0}".format(name))

    def add_row(self, new_row : str):
        logging.debug("Adding row '{0}' to Map {1}".format(new_row, self.name))
        self.layout.append(new_row)

    def print(self):
        print("Island {0}".format(self.name))
        for row in self.layout:
            print(row)


class IslandMapFactory():
    def __init__(self):
        self.islands = {}

    def load(self, data_dir : str, data_file_name : str):

        file_location = "{0}\\{1}".format(data_dir, data_file_name)

        logging.debug("Loading Island Maps from {0}".format(file_location))

        # Attempt to open the file
        with open(file_location, 'r') as object_file:

            # Load all rows in as a dictionary
            reader = csv.DictReader(object_file)

            # Get the list of column headers
            header = reader.fieldnames

            old_name = None

            # For each row in the file....
            for row in reader:
                print(str(row))
                name = row.get("Name")

                if name != old_name:
                    new_map = IslandMap(name)
                    self.islands[name] = new_map

                layout = ""

                # loop through all of the header fields except the first column...
                for i in range(1, len(header)):

                    # Get the next field value from the header row
                    field = header[i]
                    value = row.get(field)
                    if value == "":
                        value = "_"
                    layout += value

                new_map.add_row(layout)

                old_name = name

        logging.info("Loaded {0} islands".format(len(self.islands.keys())))


    def print(self):
        for island in self.islands.values():
            island.print()

