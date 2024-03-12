import json
from os.path import exists, abspath


class Profile:
    """
    This class is used to handle the profiles.json file. It is used to get, set, and add profiles to the file.
    """

    def __init__(self, path=abspath('../json_schema/profiles.json')):
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
        if self.check_file():
            with open(self.path, 'r') as file:
                data = json.load(file)
                return data
        else:
            return None

    def get_profile(self, profile_uuid):
        """
        This method returns a profile by its uuid
        :param profile_uuid:
        :return: profile matching given uuid
        """
        if self.check_file():
            try:
                with open(self.path, 'r') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["profile_uuid"] == profile_uuid:
                            return profile
            except:
                print("json error: Make sure profiles.json is formatted correctly")
        return None

    def set_profile(self, profile_uuid, profile_name, profile_color):
        """
        This method sets the profile name and/or color by the uuid
        :param profile_uuid:
        :param profile_name:
        :param profile_color:
        """
        if (profile_name or profile_color) == None:
            raise ValueError("name or color cannot be none")

        if self.check_file():
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["profile_uuid"] == profile_uuid:
                            if profile_name != None:
                                profile["profile_name"] = profile_name
                            if profile_color != None:
                                profile["profile_color"] = profile_color
                            break
                    with open(self.path, 'w') as file:
                        json.dump(data, file)
            except:
                print("json error: Make sure profiles.json is formatted correctly")
        return None

    def get_profile_by_name(self, profile_name):
        if self.check_file():
            """
            This method returns a profile by its name
            :param profile_name:
            :return: profile matching given name
            """
            try:
                with open(self.path, 'r') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["profile_name"] == profile_name:
                            return profile
            except:
                print("json error: Make sure profiles.json is formatted correctly")
        return None

    def add_new_profile(self, profile_name, profile_uuid, profile_color):
        """
        This method adds a new profile to the file
        :param profile_name:
        :param profile_uuid:
        :param profile_color:
        """
        if self.check_file():
            entry = {"profile_name": profile_name, "profile_uuid": profile_uuid, "profile_color": profile_color}
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    file.seek(0)
                    data.append(entry)
                    json.dump(data, file)
                    file.truncate()
            except:
                print("json error: Make sure profiles.json is formatted correctly")

        else:
            with open(self.path, 'w') as file:
                entry = [{"profile_name": profile_name, "profile_uuid": profile_uuid, "profile_color": profile_color}]
                json.dump(entry, file)

    def delete_profile(self, profile_uuid):
        """
        This method deletes a profile by its uuid
        :param profile_uuid:
        """
        if self.check_file():
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["profile_uuid"] == profile_uuid:
                            data.remove(profile)
                            break
                    else:
                        raise ValueError(f"Profile with given uuid: {profile_uuid} not found")
                    with open(self.path, 'w') as file:
                        json.dump(data, file)
            except:
                print("json error: Make sure profiles.json is formatted correctly")

    def delete_profile_by_name(self, profile_name):
        """
        This method deletes a profile by its name
        :param profile_name:
        """
        if self.check_file():
            try:
                with open(self.path, 'r+') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["profile_name"] == profile_name:
                            data.remove(profile)
                            break
                    else:
                        raise ValueError(f"Profile with given name: {profile_name} not found")
                    with open(self.path, 'w') as file:
                        json.dump(data, file)
            except:
                print("json error: Make sure profiles.json is formatted correctly")

    def delete_all_profiles(self):
        """
        This method deletes all profiles
        """
        if self.check_file():
            with open(self.path, 'w') as file:
                file.write("[]")

