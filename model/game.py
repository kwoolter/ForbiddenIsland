import model.island as island
import logging
import os
import random

class Game():

    GAME_DATA_DIR = os.path.dirname(__file__) + "\\data\\"

    def __init__(self):
        self.current_island = None
        self.islands = None
        self.locations = None



    def initialise(self):
        logging.info("Initialising game...")

        self.locations = island.IslandLocationFactory()
        self.locations.load(Game.GAME_DATA_DIR, "squares.csv")

        self.locations.print()

        self.islands = island.IslandMapFactory()
        self.islands.load(Game.GAME_DATA_DIR, "maps.csv")
        self.islands.print()

        logging.info("Finished Initialising game...")

    def get_island_names(self):
        return self.islands.get_island_names()

    def create_island(self, island_name : str):
        if island_name in self.islands.get_island_names():

            current_island = self.islands.get_island(island_name)

            location_names = self.locations.location_names
            while current_island.free_locations > 0:
                random_location_name = random.choice(location_names)
                current_island.add_location(self.locations.get_location(random_location_name))
                location_names.remove(random_location_name)

            current_island.print()

        else:
            raise Exception("Island {0} has not been loaded!".format(island_name))

