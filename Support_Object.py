import os.path
from FileTransform import *


class SupportClass:

    def __init__(self, error_diction):
        """
        Initiates the class with the correct attributes.
        :param error_diction: A complex dictionary with keys that have complex structures as their values.
        """
        self.error_diction = error_diction
        self.error_msgsList = ["null title.", "invalid type for title.", "invalid estimation hours.",
                               "null estimation hours.", "invalid type for estimation hours.",
                               "attraction rating out of valid range.", "invalid rating type.",
                               "type error with attraction's latitude.", "type error with attraction's longitude",
                               "conflict with attraction's opening hours.", "total attractions under 20."]

    def has_key(self, error_dict, key):
        """

        :param error_dict: A dictionary that contains all the errors that have occurred during unit testing.
        :param key: An attraction's ID, a string.
        :return: True, if the ID already exists in the dictionary; False otherwise.

        """
        key_list = error_dict.keys()
        return key in key_list

    def check_float(self, variable):
        """

        :param variable: A variable that has been passed in for type checking.
        :return: True, if Variable is of type float; False otherwise.
        """

        return isinstance(variable, float)

    def check_int(self, variable):
        """

        :param variable: A variable that has been passed in for type checking.
        :return: Boolean, True if variable is of type int; False otherwise
        """

        return isinstance(variable, int)

    def repr_errors(self, error_dict, errors_file):
        """
        Representing the error messages collected in a text file in a clean way,
        that is easy to eye-ball and process.

        :param error_dict: A dictionary that contains error messages. error_dict itself is a complex object.
        :param errors_file: A string that represents the name and the extension of the file being written.
        :return: None
        """

        if not os.path.isfile(errors_file):
            output = open(errors_file, "w")

        else:
            output = open(errors_file, "a")

        output.write(json.dumps(error_dict, indent=4))
        output.close()

    def search_location(self, loc, input):
        """
        Search the loc in the search_f and return it. Pre-condition: loc does exist in search_f.
        :param loc: String, the location that is to be searched.
        :param input: String, the name and extension of the file that is to be searched.
        :return: String, the exact location with complete info from search_f.
        """

        location = ""
        with open(input) as file:
            for line in file:
                if loc in line:
                    location = line
                    return location

    def transform_obj(self, loc_str):
        """
        Transform the location string given into a dictionary.
        :param loc_str: String, the string that contains a location's name, division, latitude and longitude.
        Ex: loc = "La Victoria, Central Region, Venezuela	South America	10.2116947	-67.324689"
        :return: Object, a dictionary that contains this location's information.
        Ex: {"location": {"lat": 10.2116947, "lon" : -67.324689}, "preferences" = [], "start" = 0,
            "division" = "South America"}
        """

        split = loc_str.split("\t")
        loc_dict = {}
        loc_dict["location"] = {}
        loc_dict["location"]["lat"] = float(split[2])
        loc_dict["location"]["lon"] = float(split[3])
        loc_dict["preferences"] = []
        loc_dict["start"] = 0
        loc_dict["division"] = split[1]

        return loc_dict

    def has_error(self, dictiona):
        """
        Detect whether the dictionary provided has an error message.
        :param dictiona: A dictionary that contains keys with lists as their values.
        Ex:
        diction = {key1: [], key2["some string", "another string"], key3:["some string", "another string",
        "very annoying string"]} etc.
        :return: Boolean, True if the dictionary contains an error, False otherwise.
        """
        for IDs in dictiona:
            if len(dictiona.get(IDs)) != 0:
                return True
        return False

    def get_errorattrs(self):

        """

        :return: None
        """
        overall_errfile = open("error_attractions.txt", "w")
        for locations in self.error_diction:
            ID_diction = self.error_diction.get(locations)[0]
            if self.has_error(ID_diction):
                # if the ID contains an error within
                overall_errfile.write(locations + ": \n")
                for ids in ID_diction:
                    # a dictionary with all attraction IDS

                    # parse every attraction, if any error messages exist
                    if len(ID_diction.get(ids)) != 0:
                        overall_errfile.write("\t"+ids+": ")
                        for every_msg in ID_diction.get(ids):
                            if ID_diction.get(ids)[-1] == every_msg:
                                overall_errfile.write(every_msg+"\n")

                            else:
                                overall_errfile.write(every_msg+", ")
                overall_errfile.write("\n")


if __name__ == "__main__":

    transformer = FileProcessing("copy_errormsgs.txt")
    diction = transformer.text_to_dict()
    support_obj = SupportClass(diction)
    support_obj.get_errorattrs()





