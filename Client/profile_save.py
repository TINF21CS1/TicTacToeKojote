import json
from os.path import exists
import os
from Server.player import Player

path=os.path.abspath('Client/Data/profiles.json')

class Profile:
    """
    This class is used to save and load profiles
    """

    @staticmethod
    def get_profiles():
        """
        This method returns a list of profiles from the file
        """
        Profile._check_folder()
        if exists(path):
            with open(path, 'r') as file:
                data = json.load(file)
                if not data:
                    return [], 0
                output = []
                profile_data = data[0]
                selected = data[1]
                for profile in profile_data:
                    output.append(Player.from_dict(profile))
                return output, selected
        else:
            return [], None

    @staticmethod
    def set_profiles(players: list, selected: int):
        """
        This method saves the profiles to the file
        """
        Profile._check_folder()
        with open(path, 'w+') as file:
                entry = []
                for player in players:
                    entry.append(player.as_dict())
                json.dump([entry, selected], file)

    @staticmethod
    def delete_all_profiles():
        """
        This method deletes all profiles
        """
        Profile._check_folder()
        if exists(path):
            with open(path, 'w') as file:
                file.write("[]")

    @staticmethod
    def _check_folder():
        """
        This method checks if the folder for the profiles exists and creates it if it doesn't
        """
        dir = os.path.abspath('Client/Data/')
        if not os.path.exists(os.path.abspath(dir)):
            try:
                os.makedirs(os.path.abspath(dir))
            except OSError:
                raise OSError(f"Creation of the directory {dir} failed")