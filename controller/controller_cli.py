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

            self.model.current_island.print_map()

            if utils.confirm("Ok with this island?") is True:
                loop = False

        # try:
        #
        #     self.model = model.Game()
        #     self.model.initialise()
        #
        # except Exception as err:
        #     print(str(err))


