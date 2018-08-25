import logging
import csv
import copy

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
        str = "{0} ({1})".format(self.name, self._state)

        if self.start is not None:
            str += ", starting location for {0}".format(self.start)

        if self.temple is not None:
            str += ", Temple for {0} treasure".format(self.temple)

        if self.is_exit is True:
            str += ", exit from the game"

        return str

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state : str):
        self._state = new_state

    def water_rise(self):

        if self.state == IslandLocation.NORMAL:
            self.state = IslandLocation.FLOODED
        elif self.state == IslandLocation.FLOODED:
            self.state = IslandLocation.SUNK

        return self.state

    def shore_up(self):
        if self.state == IslandLocation.FLOODED:
            self.state = IslandLocation.NORMAL

class IslandLocationFactory():

    def __init__(self):
        self.locations = {}

    @property
    def location_names(self):
        return list(self.locations.keys())

    def get_location(self, location_name : str):
        if location_name in self.locations.keys():
            return copy.deepcopy(self.locations[location_name])
        else:
            raise Exception("Can't find location {0} in the list of loaded locations".format(location_name))

    def get_locations(self):
        return copy.deepcopy(list(self.locations.values()))

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
                #print(str(row))
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

    LAND = "#"
    EMPTY = "_"

    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    DIRECTIONS = ( NORTH, SOUTH, EAST, WEST)
    DIRECTION_VECTORS = {NORTH : (0,-1), SOUTH: (0,1), EAST:(-1,0), WEST:(1,0)}

    def __init__(self, name: str):
        self.name = name
        self.layout = []
        self.map = None
        self.free_squares = []
        self.locations = {}
        self.explorers = {}
        self.explorer_start_locations = {}
        self.explorer_locations = {}
        self.temple_locations = {}
        self.width = 0

        #logging.debug("Constructing new map {0}".format(name))

    def __str__(self):
        return "{0} island ({1}x{2})".format(self.name, self.width, self.height)

    @property
    def height(self):
        return len(self.layout)

    @property
    def free_locations(self):
        return len(self.free_squares)

    def add_row(self, new_row : str):
        logging.debug("Adding row '{0}' to Map {1}".format(new_row, self.name))
        self.layout.append(new_row)
        self.width = max(self.width, len(new_row))

    def build_map(self):
        self.map = [[None for x in range(self.height)] for x in range(self.width)]
        y=0
        for row in self.layout:
            for x in range(0, len(row)):
                if row[x] == IslandMap.LAND:
                    self.free_squares.append((x,y))
            y += 1

    def get_location(self, x : int, y : int):

        if x<0 or x>=self.width or y<0 or y >= self.height:
            raise Exception("Get location: specified location ({0},{1}) is off the map!".format(x,y))

        return  self.map[x][y]

    def add_location(self, new_location : IslandLocation):
        if len(self.free_squares) > 0:
            x,y = self.free_squares.pop(0)
            self.map[x][y] = new_location
            self.locations[new_location.name] = new_location
            if new_location.start is not None:
                self.explorer_start_locations[new_location.start] = (x,y)
        else:
            raise Exception("Can't add location {0} as not more free squares.".format(new_location.name))

    def flood_location(self, location_name : str):
        if location_name in self.locations.keys():
            self.locations[location_name].water_rise()
            return self.locations[location_name]
        else:
            raise Exception("Flood: location: can';t find location {0} in the map".format(location_name))

    def add_explorer(self, explorer_type : str):
        if explorer_type in self.explorer_start_locations.keys():
            x,y = self.explorer_start_locations[explorer_type]
            self.explorer_locations[explorer_type] = (x,y)
            print("Adding explorer {0} to square ({1},{2})".format(explorer_type,x,y))
        else:
            raise Exception("Explorer type {0} does not have a defined starting location!")

    def move_explorer(self, explorer_type : str, direction : str):

        if explorer_type not in self.explorer_locations.keys():
            raise Exception("Move explorer: explorer type {0} not on this island!".format(explorer_type))

        if direction not in IslandMap.DIRECTIONS or direction not in IslandMap.DIRECTION_VECTORS:
            raise Exception("Moving explorer: {0} is not a valid direction!".format(direction))

        dx,dy = IslandMap.DIRECTION_VECTORS[direction]
        x,y = self.explorer_locations[explorer_type]
        new_x = x + dx
        new_y = y + dy
        new_location = self.map[new_x][new_y]
        if new_location is None:
            raise Exception("Can't move that way: Off the map!")
        elif new_location.state == IslandLocation.SUNK:
            raise Exception("Can't move that way: Location has sunk!")

        self.explorer_locations[explorer_type] = (new_x, new_y)
        print("Move {0} {0} to ({2},{3})".format(explorer_type, direction, new_x, new_y))



    def print_layout(self):
        print("{0} island ({1}x{2})".format(self.name, self.width, self.height))
        print("Layout:")
        for row in self.layout:
            print(row)

    def print_map(self):
        for y in range(0, self.height):
            row = ""
            for x in range(0, self.width):
                location = self.map[x][y]
                if location is not None:
                    if (x,y) in self.explorer_locations.values():
                        row += "@"
                    elif location.state == IslandLocation.NORMAL:
                        row += "#"
                    elif location.state == IslandLocation.FLOODED:
                        row += "~"
                    elif location.state == IslandLocation.SUNK:
                        row += "X"
                    else:
                        row += "?"

                else:
                    row += " "
            print(row)

    def print(self):
        print("{0} island ({1}x{2})".format(self.name, self.width, self.height))
        print("Map:")
        self.print_map()
        print("Added locations:")
        for y in range(0, self.height):
            for x in range(0, self.width):
                location = self.map[x][y]
                if location is not None:
                    print(str(location))

        print("Free locations = {0}".format(self.free_locations))


class IslandMapFactory():
    def __init__(self):
        self.islands = {}

    def get_island_names(self):
        return list(self.islands.keys())

    def get_island(self, island_name : str):
        if island_name in self.islands.keys():
            return self.islands[island_name]
        else:
            raise Exception("Can't find island {0} in the factory".format(island_name))

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
            new_map = None

            # For each row in the file....
            for row in reader:
                #print(str(row))

                name = row.get("Name")

                if name != old_name:
                    if new_map is not None:
                        new_map.build_map()

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

            new_map.build_map()

        logging.info("Loaded {0} islands".format(len(self.islands.keys())))


    def print(self):
        for island in self.islands.values():
            island.print()

