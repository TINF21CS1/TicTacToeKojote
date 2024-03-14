import json
from os.path import exists
import os
from Server.player import Player

path=os.path.abspath('Client/Data/profiles.json')

class Profile:
    """
    This class is used to handle the profiles.json file. It is used to get, set, and add profiles to the file.
    """


    def get_profiles():
        global path
        """
        This method returns all the profiles from the file
        :return: An array of all profiles
        """
        if exists(path):
            with open(path, 'r') as file:
                data = json.load(file)
                output = []
                profile_data = data[0]
                selected = data[1]
                for profile in profile_data:
                    output.append(Player.from_dict(profile))
                return output, selected
        else:
            return [], 0

    def set_profiles( players: list, selected: int):
        global path
        """
        This method sets the profile name and/or color by the uuid
        :param profile_uuid:
        :param profile_name:
        :param profile_color:
        """

        #try:
        with open(path, 'w') as file:
                entry = []
                for player in players:
                    entry.append(player.as_dict())
                json.dump([entry, selected], file)
        #except:
        #    raise RuntimeError("json error: Make sure profiles.json is formatted correctly")

    def delete_all_profiles():
        global path
        """
        This method deletes all profiles
        """
        if exists(path):
            with open(path, 'w') as file:
                file.write("[]")
