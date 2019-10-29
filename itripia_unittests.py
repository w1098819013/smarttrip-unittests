import requests
import json
from Supporting_Functions import *
import os.path

'''
task = {"location":{"lat":49.2827291,"lon":-123.1207375},"preferences":[],"start":0,"division":"Asia"}
resp = requests.post("https://apis.itripia.com/attraction/search_attractions", json = task)
print(json.dumps(resp.json(), indent=4))

if resp.json()['total'] < 1000:
    report = {"text": "Total attraction error"}
    resp = requests.post('https://hooks.slack.com/services/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', json = report)
'''

'''
task = {"location":{"lat":49.2827291,"lon":-123.1207375},"preferences":[], "start":0, "division":"North America"}
resp = requests.post('https://apis.itripia.com/attraction/search_attractions',json=task)
print(json.dumps(resp.json(), indent=4))
'''


def test_attractions(start, test_range, input_file):
    """
    Test each location's attractions to ensure the correctness of every piece of information.
    Collect error information along the way and output the info onto a txt file for future referencing.

    :param start: String, starting location of the current test. Empty string if test has never been initialized.
    :param test_range: Int, The number of cities to be tested.
    :param input_file: String, the name of the file that contains all the cities.
    :return: Int, the line counter of the very last location in the input_file, or None.
    """

    in_file = open(input_file, "rt")

    in_file.readline()
    error_dict = {}
    line = ""
    # Go to the location that the test ended off at last time by reading lines one by one.
    while line != start:
        # loop exits when line reaches the location that was ended off last time
        line = in_file.readline()

    for line_count in range(test_range):
        sequence_lines = in_file.readline()

        if line_count == test_range - 1:
            record_file = open("test_records.txt", "w")
            record_file.write(sequence_lines)

            #if sequence_lines == "":
            #    line_count += 2
             #   return line_count
        if sequence_lines == "":
            break

        task = {}
        split = sequence_lines.strip().split("\t")
        # strip the line break at the tail, then split the string by \t
        task["location"] = {}
        task["location"]["lat"] = float(split[2])
        task["location"]["lon"] = float(split[3])
        task["preferences"] = []
        task["start"] = 0
        task["division"] = split[1]

        resp = requests.post('https://apis.itripia.com/attraction/search_attractions', json=task)
        error_dict[split[0]] = [{}]

        for attraction in resp.json()['attractions']:
            if not has_key(error_dict[split[0]][0], attraction["id"]):
                error_dict[split[0]][0][attraction["id"]] = []

            if attraction['title'] is None:
                # Attraction title
                # take the ID and store it somewhere for future error reporting
                error_dict[split[0]][0][attraction["id"]].append("null title.")

            if attraction["title"].isdigit() is True:
                # Do the same as above
                error_dict[split[0]][0][attraction["id"]].append("invalid type for title.")

            if attraction["estimation_hours"] <= 0:
                # estimation hours
                # take the ID and store it somewhere for future error reporting
                error_dict[split[0]][0][attraction["id"]].append("invalid estimation hours.")

            if not isinstance(attraction["estimation_hours"], (float, int)):

                if attraction["estimation_hours"] is None:
                    # Do the same as above
                    error_dict[split[0]][0][attraction["id"]].append("null estimation hours.")

                else:
                    error_dict[split[0]][0][attraction["id"]].append("invalid type for estimation hours.")

            if attraction["rating"] < 0 or attraction["rating"] > 5:
                # rating
                # take the ID and store it somewhere for future error reporting
                error_dict[split[0]][0][attraction["id"]].append("attraction rating out of valid range.")

            if not isinstance(attraction["rating"], float):
                # Do the same as above
                error_dict[split[0]][0][attraction["id"]].append("invalid rating type.")

            if not isinstance(attraction["location"]["geometry"]["lat"], float):
                # Keep error
                error_dict[split[0]][0][attraction["id"]].append("type error with attraction's latitude.")

            if not isinstance(attraction["location"]["geometry"]["lon"], float):
                # Keep error
                error_dict[split[0]][0][attraction["id"]].append("type error with attraction's longitude.")

            if "opening_hours" in attraction.keys():
                for days in attraction["opening_hours"]:
                    # opening_hours is a list of dictionaries, each dictionary represents one day
                    if not days["opens"]:
                        # if the attraction is not opened on that day
                        if "start" in days.keys() or "end" in days.keys():
                            # Keep error
                            # error_msg.write("ID: "+attraction["id"]+" conflict with attraction's opening hours.\n")
                            error_dict[split[0]][0][attraction["id"]].append("conflict with attraction's opening hours.")

        if resp.json()['total'] < 20:
            # checking if total attractions are under 20
            error_dict[split[0]].append("total attractions under 20.")


    in_file.close()
    repr_errors(error_dict, "error_msgs.txt")


def record_test(test_range, input_file, record_file):
    """
    Test each location's attractions to ensure the correctness of every piece of information. Starts from the
    first location if test has never been initialized, last ended location otherwise.
    Collect error information along the way and output the info onto a txt file for future referencing.

    :param test_range: Int, the number of locations to be tested for the following test.
    :param input_file: String, the text file that contains all locations that should be tested.
    :param record_file: String, the text file that contains the ending location from the last test.
    :return: None
    """
    result = None

    if not (os.path.isfile(record_file)):
        # If test hasn't been initialized before
        result = test_attractions("", test_range, input_file)

    else:
        # if test_records.txt exists
        record_f = open(record_file, "rt")
        start_loc = record_f.readline()
        result = test_attractions(start_loc, test_range, input_file)

    if result:
        # If unittest returns an integer other than nothing
        write_lastloc(result, input_file, record_file)

if __name__ == "__main__":
    record_test("", "tobe_retested.txt", "test_records.txt")




