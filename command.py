from api import *
from flask_script import Manager, Command
from api.commands.users import UserCreateCommand

manager = Manager(app)

	

class Hello(Command):
    "prints hello world"

    def run(self):
        print("hello world")

if __name__ == "__main__":
    manager.add_command('create-user', UserCreateCommand())
    manager.run()
