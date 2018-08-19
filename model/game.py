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

        current_island = self.islands.get_island("Basic")

        location_names = self.locations.location_names
        while current_island.free_locations > 0:
            random_location_name = random.choice(location_names)
            current_island.add_location(self.locations.get_location(random_location_name))
            location_names.remove(random_location_name)

        #self.islands.print()
        current_island.print()


        logging.info("Finished Initialising game...")