import model.island as island
import logging
import os
import random

class Game():

    EXPLORER_DIVER = "Diver"
    EXPLORER_PILOT = "Pilot"
    EXPLORER_ENGINEER = "Engineer"
    EXPLORER_TYPES = (EXPLORER_DIVER, EXPLORER_ENGINEER, EXPLORER_PILOT)

    GAME_DATA_DIR = os.path.dirname(__file__) + "\\data\\"

    def __init__(self):
        self._current_island = None
        self.islands = None
        self.locations = None
        self.explorers = None

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
        self.islands.print()

        self.explorers = []

        logging.info("Finished Initialising game...")

    def get_island_names(self):
        return self.islands.get_island_names()

    def create_island(self, island_name : str):
        if island_name in self.islands.get_island_names():

            self.current_island = self.islands.get_island(island_name)

            location_names = self.locations.location_names
            while self.current_island.free_locations > 0:
                random_location_name = random.choice(location_names)
                self.current_island.add_location(self.locations.get_location(random_location_name))
                location_names.remove(random_location_name)

        else:
            raise Exception("Island {0} has not been loaded!".format(island_name))


    def add_explorer(self, explorer_type : str):

        if explorer_type in Game.EXPLORER_TYPES:
            self.explorers.append(explorer_type)
        else:
            raise Exception("Unknown explorer type {0}".format(explorer_type))