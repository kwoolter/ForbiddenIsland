import model.island as island
import logging
import os
import random
import copy
import math

class Game():

    ADVENTURER_DIVER = "Diver"
    ADVENTURER_PILOT = "Pilot"
    ADVENTURER_ENGINEER = "Engineer"
    ADVENTURER_MESSENGER = "Messenger"
    ADVENTURER_NAVIGATOR = "Navigator"
    ADVENTURER_EXPLORER = "Explorer"
    ADVENTURER_TYPES = (ADVENTURER_DIVER, ADVENTURER_ENGINEER, ADVENTURER_PILOT, ADVENTURER_MESSENGER, ADVENTURER_NAVIGATOR, ADVENTURER_EXPLORER)

    GAME_DATA_DIR = os.path.dirname(__file__) + "\\data\\"

    def __init__(self):
        self._current_island = None
        self.islands = None
        self.locations = None
        self.adventurers = None

        self.location_deck = None
        self.location_deck_discard = None

    @property
    def current_island(self):
        return self._current_island

    @current_island.setter
    def current_island(self, new_island : island.IslandMap):
        self._current_island = new_island


    def initialise(self):
        logging.info("Initialising game...")

        self.locations = island.IslandLocationFactory()
        self.locations.load(Game.GAME_DATA_DIR, "squares.csv")

        self.locations.print()

        self.islands = island.IslandMapFactory()
        self.islands.load(Game.GAME_DATA_DIR, "maps.csv")
        #self.islands.print()

        self.adventurers = []

        self.location_deck = self.locations.get_locations()
        random.shuffle(self.location_deck)
        self.location_deck_discard = []



        logging.info("Finished Initialising game...")

    def get_island_names(self):
        return self.islands.get_island_names()

    def create_island(self, island_name : str):
        if island_name in self.islands.get_island_names():

            self.current_island = self.islands.get_island(island_name)

            location_names = self.locations.location_names

            if len(location_names) < self.current_island.free_locations:
                raise Exception("Error trying to add {0} locations to a map with {1} sqaures.".format(len(location_names),self.current_island.free_locations))

            while self.current_island.free_locations > 0:
                random_location_name = random.choice(location_names)
                self.current_island.add_location(self.locations.get_location(random_location_name))
                location_names.remove(random_location_name)

            for i in range(1, 6):
                self.deal_location()

        else:
            raise Exception("Island {0} has not been loaded!".format(island_name))


    def add_adventurer(self, adventurer_type : str):

        if adventurer_type in Game.ADVENTURER_TYPES:
            if adventurer_type not in self.adventurers:
                self.adventurers.append(adventurer_type)
                self.current_island.add_adventurer(adventurer_type)
            else:
                raise Exception("Explorer type {0} already added to the game!".format(adventurer_type))
        else:
            raise Exception("Unknown explorer type {0}".format(adventurer_type))

    def get_directions(self, adventurer_type : str = None):
        valid_directions = []
        for direction, vector in island.IslandMap.DIRECTION_VECTORS.items():
            x,y = vector
            length = math.sqrt(x*x + y*y)
            if adventurer_type == Game.ADVENTURER_EXPLORER or length <= 1:
                valid_directions.append(direction)

        return valid_directions


    def move_adventurer(self, explorer_type : str, direction : str):
        self.current_island.move_adventurer(explorer_type, direction)

    def deal_location(self):
        new_location = self.location_deck.pop(0)

        map_location = self.current_island.flood_location(new_location.name)
        if map_location.state != island.IslandLocation.SUNK:
            self.location_deck_discard.append(new_location)

        return new_location

    def merge_location_decks(self):
        self.location_deck = self.location_deck_discard + self.location_deck
        self.location_deck_discard = []

    def print(self):

        self.current_island.print()
        print("Location deck:")
        for location in self.location_deck:
            print(location)

        print("Location discard deck:")
        for location in self.location_deck_discard:
            print(location)

    def print_map(self):
        self.current_island.print_map()