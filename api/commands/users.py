
from flask_script import Command
import click
import getpass

from api.models.user import UserModel

class UserCreateCommand(Command):
    """Create a user"""
    def run(self):
        username = input("Username: ")
        email = input("Email: ")
        is_admin = input("Is admin? [y/n]: ")
        password = getpass.getpass("Password: ")
        roles = ["admin"] if is_admin.lower() == 'y' else []

        try:
            new_user = UserModel(
                username = username,
                email = email,
                password = UserModel.generate_hash(password)
            )
            new_user.roles = roles
            new_user.save_to_db()

            print('\n+ User created')
            print('|_ Username: {}'.format(new_user.username))
            print('|_ Email:    {}'.format(new_user.email))
            print('|_ Roles:    {}'.format(new_user.roles))
        except:
            print('User wasn\'t saved')
