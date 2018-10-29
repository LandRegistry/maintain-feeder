from manager import Manager
from maintain_feeder.main import run

manager = Manager()


@manager.command
def runserver(port=9198):
    """Run the app using flask server"""
    run()


if __name__ == "__main__":
    manager.main()
