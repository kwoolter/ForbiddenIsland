import model.island as island
import logging

class Game():

    def __init__(self):
        self.current_island = None
        self.islands = None



    def initialise(self):
        logging.info("Initialising game...")

        self.islands = island.IslandFactory()
        self.islands.load()

        logging.info("Finished Initialising game...")