import json
from os.path import exists
import os
from Server.player import Player


class Profile:
    """
    This class is used to handle the profiles.json file. It is used to get, set, and add profiles to the file.
    """

    def __init__(self, path=os.path.abspath('Client/Data/profiles.json')):
        self.path = path

    def get_profiles(self):
        """
        This method returns all the profiles from the file
        :return: An array of all profiles
        """
        if exists(self.path):
            with open(self.path, 'r') as file:
                data = json.load(file)
                output = []
                for profile in data:
                    output.append(Player.from_dict(profile))
                return output
        else:
            return []

    def set_profiles(self, players: list):
        """
        This method sets the profile name and/or color by the uuid
        :param profile_uuid:
        :param profile_name:
        :param profile_color:
        """

        try:
            with open(self.path, 'w') as file:
                entry = []
                for player in players:
                    entry.append(player.as_dict())
                json.dump(entry, file)
        except:
            raise RuntimeError("json error: Make sure profiles.json is formatted correctly")

    def delete_all_profiles(self):
        """
        This method deletes all profiles
        """
        if exists(self.path):
            with open(self.path, 'w') as file:
                file.write("[]")
