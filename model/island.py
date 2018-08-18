import logging
import csv


class Island():
    def __init__(self, name :str):
        self.name = name
        self.map = None

class IslandLocation():
    def __init__(self, name : str, start : str, temple : str, is_exit : str):
        self.name = name
        self.start = start
        self.temple = temple

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

class IslandMapFactory():
    def __init__(self):
        self.islands = {}


    def load(self, data_dir : str, data_file_name : str):

        logging.info("Loading Islands...")

        island_name = "Basic"
        island_map = []

        self.islands[island_name] = island_map

        island_name = "Skull Island"
        island_map = []

        self.islands[island_name] = island_map

        logging.info("Loaded {0} islands".format(len(self.islands.keys())))

