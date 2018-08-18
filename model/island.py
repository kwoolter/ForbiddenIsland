import logging


class Island():
    def __init__(self, name :str):
        self.name = name



class IslandFactory():
    def __init__(self):
        self.islands = {}


    def load(self):

        logging.info("Loading Islands...")

        island_name = "Basic"
        island_map = []

        self.islands[island_name] = island_map

        logging.info("Loaded {0} islands".format(len(self.islands.keys())))

