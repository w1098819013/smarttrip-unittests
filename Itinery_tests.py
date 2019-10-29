import requests
import json
from Supporting_Functions import *
from itripia_unittests import *

task = {
  "travel_date": "10/24/2017",
  "day_start_time": 480,
  "start_from_airport": False,
  "tightness": 1,
  "origin": {
    "title": "Ripley's Aquarium Of Canada",
    "estimation_hours": 1.5,
    "imageUrl": "//d2ufymg9xaenll.cloudfront.net/static/images/google_attractions/5738eedd54fb5f10b8c2d2a3/CoQBdwAAACqWzfZw1KukTBMed4DEDmFKbQabvyQkIel_LJaGpkKDG51dnCtMJvaCPHnsfQCCf7f_qpG950upAmYbBpIsR2KbsgjlTXKYTQ_dzYsgr8xsbUXGKniL-nlsJSmK49oHwiiSMMP6y8glZlw0A-eawGqqBaQLBZX0ykHbibQvlUTcEhBmBVVXBpOuyEke0vVA3z8UGhSHzoiCMSDhI96IFPnxasCJ_uSQDA.jpg",
    "location": {
      "id": "5738eedd54fb5f10b8c2d2a3",
      "province": "Ontario",
      "province_abbr": "ON",
      "city": "Toronto",
      "country": "Canada",
      "division": "North America",
      "google_place_id": "ChIJWwS21dU0K4gRPSGMKRkar40",
      "google_url": "https://maps.google.com/?cid=10209407575645757757",
      "location": {},
      "formatted_address": "288 Bremner Blvd, Toronto, ON M5V 3L9, Canada",
      "geometry": {
        "lat": 43.64245369999999,
        "lon": -79.3861234
      },
      "opening_hours": [
        {
          "day": "Monday",
          "opens": True,
          "start": "9:00 AM",
          "end": "9:00 PM"
        }
      ]
    }
  },
  "destination": {
    "title": "Ripley's Aquarium Of Canada",
    "estimation_hours": 1.5,
    "imageUrl": "//d2ufymg9xaenll.cloudfront.net/static/images/google_attractions/5738eedd54fb5f10b8c2d2a3/CoQBdwAAACqWzfZw1KukTBMed4DEDmFKbQabvyQkIel_LJaGpkKDG51dnCtMJvaCPHnsfQCCf7f_qpG950upAmYbBpIsR2KbsgjlTXKYTQ_dzYsgr8xsbUXGKniL-nlsJSmK49oHwiiSMMP6y8glZlw0A-eawGqqBaQLBZX0ykHbibQvlUTcEhBmBVVXBpOuyEke0vVA3z8UGhSHzoiCMSDhI96IFPnxasCJ_uSQDA.jpg",
    "location": {
      "id": "5738eedd54fb5f10b8c2d2a3",
      "province": "Ontario",
      "province_abbr": "ON",
      "city": "Toronto",
      "country": "Canada",
      "division": "North America",
      "google_place_id": "ChIJWwS21dU0K4gRPSGMKRkar40",
      "google_url": "https://maps.google.com/?cid=10209407575645757757",
      "location": {},
      "formatted_address": "288 Bremner Blvd, Toronto, ON M5V 3L9, Canada",
      "geometry": {
        "lat": 43.64245369999999,
        "lon": -79.3861234
      },
      "opening_hours": [
        {
          "day": "Monday",
          "opens": True,
          "start": "9:00 AM",
          "end": "9:00 PM"
        }
      ]
    }
  },
  "attractions": [
    {
      "title": "Ripley's Aquarium Of Canada",
      "estimation_hours": 1.5,
      "imageUrl": "//d2ufymg9xaenll.cloudfront.net/static/images/google_attractions/5738eedd54fb5f10b8c2d2a3/CoQBdwAAACqWzfZw1KukTBMed4DEDmFKbQabvyQkIel_LJaGpkKDG51dnCtMJvaCPHnsfQCCf7f_qpG950upAmYbBpIsR2KbsgjlTXKYTQ_dzYsgr8xsbUXGKniL-nlsJSmK49oHwiiSMMP6y8glZlw0A-eawGqqBaQLBZX0ykHbibQvlUTcEhBmBVVXBpOuyEke0vVA3z8UGhSHzoiCMSDhI96IFPnxasCJ_uSQDA.jpg",
      "location": {
        "id": "5738eedd54fb5f10b8c2d2a3",
        "province": "Ontario",
        "province_abbr": "ON",
        "city": "Toronto",
        "country": "Canada",
        "division": "North America",
        "google_place_id": "ChIJWwS21dU0K4gRPSGMKRkar40",
        "google_url": "https://maps.google.com/?cid=10209407575645757757",
        "location": {},
        "formatted_address": "288 Bremner Blvd, Toronto, ON M5V 3L9, Canada",
        "geometry": {
          "lat": 43.64245369999999,
          "lon": -79.3861234
        },
        "opening_hours": [
          {
            "day": "Monday",
            "opens": True,
            "start": "9:00 AM",
            "end": "9:00 PM"
          }
        ]
      }
    }
  ]
}
resp = requests.post("https://apis.itripia.com/itinerary/generate_itinerary", json = task)
print(json.dumps(resp.json(), indent=4))


def test_generating(resp):
    """
    Test the itinerary generating process to ensure that every piece of info in each field is correct.
    Collect all the error messages that occurred along the way, and output the messages onto a txt file
    for future referencing.

    :param task: A dictionary that contains the information of the itinerary that is to be generated.
    :return: None
    """
    errors = []
    if not check_int(resp["tightness"]):
        errors.append("Invalid type for Itinerary response's 'tightness' field.")

    if not isinstance(resp, bool):
        errors.append("Invalid type for Itinerary response's 'start_from_airport' field.")



