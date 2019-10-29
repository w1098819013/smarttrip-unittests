from Support_Object import *
import requests


class FileProcessing:

    def __init__(self, error_msgFile):
        self.error_msgFile = error_msgFile
        self.error_msgList = ["null title.","invalid type for title.", "invalid estimation hours.", "null estimation hours."
             , "invalid type for estimation hours.", "attraction rating out of valid range.",
             "invalid rating type.", "type error with attraction's latitude", "type error with attraction's longitude",
             "conflict with attraction's opening hours.", "total attractions under 20."]

    def create_dictionary(self, line):
        """
        If the line is a single character "{" with no tabs, line breaks or spaces, create a dictionary and return it.
        :param line: A string.
        :return: Dictionary, an empty dictionary, or None.
        """
        if line == "{":
            diction = {}
            return diction
        return None

    def check_loc(self, line):
        """
        If the line contains 2 commas, which means that it is a location, then set a key in diction as this location,
        and set its value to a list with an empty nested dictionary.
        :param line: A string.
        :return: The location string, or None if line is not a location
        """
        comma_count = 0
        for char in line:
            if char == ",":
                comma_count += 1
        return comma_count == 2

    def check_attr(self, line):
        """
        If the line contains 5 or more digits, then it is a attraction's ID. Set the ID as a key in the dictionary and
        its value as an empty list.
        :param diction: A dictionary
        :param line: A string
        :return: String, line if line is an attraction ID, None otherwise.
        """
        digit_count = 0
        for char in line:
            if char.isdigit():
                digit_count += 1
        return digit_count >= 5

    def check_errormsg(self, line):
        """
        Return True if line is an error message, False otherwise.
        :param line:
        :return: True if line is in self.error_msgList, False otherwise.
        """
        if line in self.error_msgList:
            return True
        return False

    def assert_location(loc):
        """
        :param loc: An object that contains all data about the location to be tested.
        Example: loc = {"location":{"lat":59.9744373,"lon":23.435507},"preferences":[], "start":0, "division":"Europe"}
        :return: The object containing the errors.
        """

        resp = requests.post('https://apis.itripia.com/attraction/search_attractions', json=loc)
        error_dict = {}
        supporter = SupportClass(loc)

        for attraction in resp.json()['attractions']:
            if not supporter.has_key(error_dict, attraction["id"]):
                error_dict[attraction["id"]] = []

            if attraction['title'] is None:
                # Attraction title
                # take the ID and store it somewhere for future error reporting
                error_dict[attraction["id"]].append("null title.")

            if attraction["title"].isdigit() is True:
                # Do the same as above
                error_dict[attraction["id"]].append("invalid type for title.")

            if attraction["estimation_hours"] <= 0:
                # estimation hours
                # take the ID and store it somewhere for future error reporting
                error_dict[attraction["id"]].append("invalid estimation hours.")

            if not isinstance(attraction["estimation_hours"], (float, int)):

                if attraction["estimation_hours"] is None:
                    # Do the same as above
                    error_dict[attraction["id"]].append("null estimation hours.")

                else:
                    error_dict[attraction["id"]].append("invalid type for estimation hours.")

            if attraction["rating"] < 0 or attraction["rating"] > 5:
                # rating
                # take the ID and store it somewhere for future error reporting
                error_dict[attraction["id"]].append("attraction rating out of valid range.")

            if not isinstance(attraction["rating"], float):
                # Do the same as above
                error_dict[attraction["id"]].append("invalid rating type.")

            if not isinstance(attraction["location"]["geometry"]["lat"], float):
                # Keep error
                error_dict[attraction["id"]].append("type error with attraction's latitude")

            if not isinstance(attraction["location"]["geometry"]["lon"], float):
                # Keep error
                error_dict[attraction["id"]].append("type error with attraction's longitude")

            if "opening_hours" in attraction.keys():
                for days in attraction["opening_hours"]:
                    # opening_hours is a list of dictionaries, each dictionary represents one day
                    if not days["opens"]:
                        # if the attraction is not opened on that day
                        if "start" in days.keys() or "end" in days.keys():
                            # Keep error
                            # error_msg.write("ID: "+attraction["id"]+" conflict with attraction's opening hours.\n")
                            error_dict[attraction["id"]].append("conflict with attraction's opening hours.")

        if resp.json()['total'] < 20:
            # checking if total attractions are under 20
            error_dict["Total Attractions"] = "total attractions under 20"

        return error_dict

    def text_to_dict(self):
        """
        Read the content in self.error_msgFile, and process the information into a complex object.
        :return: A dictionary that contains all information from self.error_msgFile in the right fields.
        """
        diction = {}
        location = ""
        attr_ID = ""
        with open(self.error_msgFile) as input_file:
            for line in input_file:
                format_str = line.replace('"', "").rstrip("\n")
                format_str = format_str.replace("\\", "")
                if self.create_dictionary(format_str) is not None:
                    diction = {}
                # print(self.set_lockey(diction, s))
                if self.check_loc(format_str):
                    location = format_str.lstrip().rstrip(": [\n")
                    diction[location] = [{}]
                if self.check_attr(format_str):
                    attr_ID = format_str.rstrip(": [\n")
                    attr_ID = attr_ID.rstrip(": []\n")
                    attr_ID = attr_ID.lstrip().rstrip(": [],\n")
                    diction[location][0][attr_ID] = []
                if self.check_errormsg(format_str.lstrip()):
                    if format_str.lstrip() == "total attractions under 20." :
                        diction[location].append(format_str.lstrip())
                    else:
                        diction[location][0][attr_ID].append(format_str.lstrip())
            input_file.close()
        return diction


#if __name__ == "__main__":




