import model.island as island
import logging
import os
import random
import copy

class Game():

    EXPLORER_DIVER = "Diver"
    EXPLORER_PILOT = "Pilot"
    EXPLORER_ENGINEER = "Engineer"
    EXPLORER_MESSENGER = "Messenger"
    EXPLORER_NAVIGATOR = "Navigator"
    EXPLORER_EXPLORER = "Explorer"
    EXPLORER_TYPES = (EXPLORER_DIVER, EXPLORER_ENGINEER, EXPLORER_PILOT, EXPLORER_MESSENGER, EXPLORER_NAVIGATOR, EXPLORER_EXPLORER)

    GAME_DATA_DIR = os.path.dirname(__file__) + "\\data\\"

    def __init__(self):
        self._current_island = None
        self.islands = None
        self.locations = None
        self.explorers = None

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

        self.explorers = []

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

        else:
            raise Exception("Island {0} has not been loaded!".format(island_name))


    def add_explorer(self, explorer_type : str):

        if explorer_type in Game.EXPLORER_TYPES:
            if explorer_type not in self.explorers:
                self.explorers.append(explorer_type)
                self.current_island.add_explorer(explorer_type)
            else:
                raise Exception("Explorer type {0} already added to the game!".format(explorer_type))
        else:
            raise Exception("Unknown explorer type {0}".format(explorer_type))

    def move_explorer(self, explorer_type : str, direction : str):
        self.current_island.move_explorer(explorer_type, direction)

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