import logging
import controller


def main():

    logging.basicConfig(level=logging.DEBUG)


    c = controller.GameCLI()
    c.cmdloop()

    return


if __name__ == "__main__":
    main()
    exit(0)