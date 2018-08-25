import cmd
import model
import utils


class GameCLI(cmd.Cmd):
    intro = "Welcome to Forbidden Island.\nType 'start' to get going!\nType 'help' for a list of commands."
    prompt = "What next?"

    def __init__(self):

        super(GameCLI, self).__init__()

        self.model = None


    def do_start(self, args):
        """Start the game"""

        self.model = model.Game()
        self.model.initialise()

        loop = True

        while loop is True:
            island_names = self.model.get_island_names()

            chosen_island = utils.pick("Island", island_names)
            self.model.create_island(chosen_island)

            self.model.current_island.print_layout()

            if utils.confirm("Ok with this island?") is True:
                loop = False

        # try:
        #
        #     self.model = model.Game()
        #     self.model.initialise()
        #
        # except Exception as err:
        #     print(str(err))

    def do_add(self,args):
        """Add an explorer"""
        try:
            new_exlorer_type = utils.pick("Explorer", model.Game.EXPLORER_TYPES)
            self.model.add_explorer(new_exlorer_type)
        except Exception as err:
            print(str(err))
    def do_move(self, args):

        try:
            explorer_type = utils.pick("Explorer", self.model.explorers, auto_pick=True)
            direction = utils.pick("Direction", model.IslandMap.DIRECTIONS)
            self.model.move_explorer(explorer_type, direction)
        except Exception as err:
            print(str(err))

    def do_draw(self, args):
        """Draw a card the game"""
        new_location = self.model.deal_location()

        print(str(new_location))



    def do_merge(self, args):
        """Merge decks"""
        self.model.merge_location_decks()

    def do_map(self, args):
        """Print the game"""
        self.model.print_map()

    def do_print(self, args):
        """Print the game"""
        self.model.print()