import cmd
import model


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

        try:

            self.model = model.Game()
            self.model.initialise()

        except Exception as err:
            print(str(err))


