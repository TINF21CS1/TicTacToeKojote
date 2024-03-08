import json
from os.path import exists

# Path to the profiles.json file
path = ('../json_schema/profiles.json')

class Profile:
    """
    This class is used to handle the profiles.json file. It is used to get, set, and add profiles to the file.
    """
    def check_file(self):
        """
        This method checks if the file exists
        :return: True if the file exists, False if it does not
        """
        if exists(path):
            print("found")
            return True
        else:
            print("not found")
            return False

    def get_profiles(self):
        """
        This method returns all the profiles from the file
        :return: An array of all profiles
        """
        if self.check_file():
            with open(path, 'r') as file:
                data = json.load(file)
                return data
        else:
            return None
    def get_profile(self,profile_uuid):
        """
        This method returns a profile by its uuid
        :param profile_uuid:
        :return: profile matching given uuid
        """
        if self.check_file():
            try:
                with open(path, 'r') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["profile_uuid"] == profile_uuid:
                            return profile
            except:
                print("json error: Make sure profiles.json is formatted correctly")
        return None
    def set_profile(self, profile_uuid , profile_name, profile_color):
        """
        This method sets the profile name and/or color by the uuid
        :param profile_uuid:
        :param profile_name: *optional*
        :param profile_color: *optional*
        """
        if profile_name == None || profile_color == None:
            raise ValueError("name or color cannot be none")
        
        if self.check_file():
            try:
                with open(path, 'r+') as file:
                    data = json.load(file)
                    for profile in data:
                        if profile["profile_uuid"] == profile_uuid:
                            profile["profile_name"] = profile_name
                            profile["profile_color"] = profile_color
                            break
                    with open(path, 'w') as file:
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
                with open(path, 'r') as file:
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
                with open(path, 'r+') as file:
                    data = json.load(file)
                    file.seek(0)
                    data.append(entry)
                    json.dump(data, file)
                    file.truncate()
            except:
                print("json error: Make sure profiles.json is formatted correctly")

        else:
            with open(path, 'w') as file:
                entry = [{"profile_name": profile_name, "profile_uuid": profile_uuid, "profile_color": profile_color}]
                json.dump(entry, file)

#Testing
#profile = Profile()
#profile.add_new_profile("test", "test", "test")
#print(profile.get_profiles())
#print(profile.get_profile("test"))
#profile.set_profile("test", "test2", "test3")
#print(profile.get_profiles())
