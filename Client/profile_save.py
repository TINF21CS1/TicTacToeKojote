import json
from os.path import exists
import os
from Server.player import Player

path=os.path.abspath('Client/Data/profiles.json')

class Profile:
    """
    This class is used to handle the profiles.json file. It is used to get, set, and add profiles to the file.
    """

    @staticmethod
    def get_profiles():
        """
        This method returns all the profiles from the file
        :return: An array of all profiles
        """
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
            return [], 0

    @staticmethod
    def set_profiles(players: list, selected: int):
        with open(path, 'w') as file:
                entry = []
                for player in players:
                    entry.append(player.as_dict())
                json.dump([entry, selected], file)

    @staticmethod
    def delete_all_profiles():
        """
        This method deletes all profiles
        """
        if exists(path):
            with open(path, 'w') as file:
                file.write("[]")
