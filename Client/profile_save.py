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

    def check_file(self):
        """
        This method checks if the file exists
        :return: True if the file exists, False if it does not
        """
        if exists(self.path):
            return True
        else:
            return False

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
            return None

    def get_profile(self, player : Player):
        """
        This method returns a profile by its uuid
        :param profile_uuid:
        :return: profile matching given uuid
        """
        player_dict = player.as_dict()
        if self.check_file():
            try:
                with open(self.path, 'r') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["uuid"] == player_dict["uuid"]:
                            return Player.from_dict(profile)
            except:
                raise RuntimeError("json error: Make sure profiles.json is formatted correctly")
        return None

    def set_profile(self, player : Player):
        """
        This method sets the profile name and/or color by the uuid
        :param profile_uuid:
        :param profile_name:
        :param profile_color:
        """
        player_dict = player.as_dict()
        if (player_dict['display_name'] or player_dict['color']) == None:
            raise ValueError("name or color cannot be none")

        if self.check_file():
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["uuid"] == player_dict["uuid"]:
                            if player_dict['display_name'] != None:
                                profile["display_name"] = player_dict['display_name']
                            if player_dict['color'] != None:
                                profile["color"] = player_dict['color']
                            break
                    with open(self.path, 'w') as file:
                        json.dump(data, file)
            except:
                raise RuntimeError("json error: Make sure profiles.json is formatted correctly")
        return None

    def set_profiles(self, players: list):
        """
        This method sets the profile name and/or color by the uuid
        :param profile_uuid:
        :param profile_name:
        :param profile_color:
        """

        if self.check_file():
            try:
                with open(self.path, 'w') as file:
                    entry = []
                    for player in players:
                        entry.append(player.as_dict())
                    json.dump(entry, file)
            except:
                raise RuntimeError("json error: Make sure profiles.json is formatted correctly")
        return None

    def get_profile_by_name(self, player : Player):
        if self.check_file():
            """
            This method returns a profile by its name
            :param profile_name:
            :return: profile matching given name
            """
            player_dict = player.as_dict()
            try:
                with open(self.path, 'r') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["display_name"] == player_dict["display_name"]:
                            return Player.from_dict(profile)
            except:
                print("json error: Make sure profiles.json is formatted correctly")
        return None

    def add_new_profile(self, player : Player):
        """
        This method adds a new profile to the file
        :param profile_name:
        :param profile_uuid:
        :param profile_color:
        """
        if self.check_file():
            entry = player.as_dict()
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    file.seek(0)
                    data.append(entry)
                    json.dump(data, file)
                    file.truncate()
            except:
                raise RuntimeError("json error: Make sure profiles.json is formatted correctly")

        else:
            with open(self.path, 'w') as file:
                entry = [player.as_dict()]
                json.dump(entry, file)

    def delete_profile(self, player : Player):
        """
        This method deletes a profile by its uuid
        :param profile_uuid:
        """
        player_dict = player.as_dict()
        if self.check_file():
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["uuid"] == player_dict["uuid"]:
                            data.remove(profile)
                            break
                    else:
                        raise ValueError(f"Profile with given uuid: {player_dict['uuid']} not found")
                    with open(self.path, 'w') as file:
                        json.dump(data, file)
            except:
                raise RuntimeError("json error: Make sure profiles.json is formatted correctly")

    def delete_profile_by_name(self, player : Player):
        """
        This method deletes a profile by its name
        :param profile_name:
        """
        player_dict = player.as_dict()
        if self.check_file():
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["display_name"] == player_dict["display_name"]:
                            data.remove(profile)
                            break
                    else:
                        raise ValueError(f"Profile with given name: {player_dict['display_name']} not found")
                    with open(self.path, 'w') as file:
                        json.dump(data, file)
            except:
                raise RuntimeError("json error: Make sure profiles.json is formatted correctly")

    def delete_all_profiles(self):
        """
        This method deletes all profiles
        """
        if exists(self.path):
            with open(self.path, 'w') as file:
                file.write("[]")

