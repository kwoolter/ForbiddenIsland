import model.island as island
import logging
import os

class Game():

    GAME_DATA_DIR = os.path.dirname(__file__) + "\\data\\"

    def __init__(self):
        self.current_island = None
        self.islands = None
        self.locations = None



    def initialise(self):
        logging.info("Initialising game...")

        self.islands = island.IslandMapFactory()
        self.islands.load(Game.GAME_DATA_DIR, "maps.csv")
        self.islands.print()

        self.locations = island.IslandLocationFactory()
        self.locations.load(Game.GAME_DATA_DIR, "squares.csv")

        self.locations.print()

        logging.info("Finished Initialising game...")