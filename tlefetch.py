# tlefetch.py is is a library that provides functionality
# of fetching a set of TLE's from a webpage for use in other parts of the program
#
# written by Ryan Deaton (rad53@calvin.edu) for Calvin Hackathon '26 on March 2026

import requests


def fetch_tles(url):
    response = requests.get(url)
    response.raise_for_status() # checks for a web error

    data = response.text.strip().splitlines()
    satelites = dict()

    # goes by threes and skips the final two.
    for i in range(0, len(data) - 2, 3):
        name  = data[i].strip()
        line1 = data[i + 1].strip()
        line2 = data[i + 2].strip()
        satelites[name] = {
            "line1": line1,
            "line2": line2
        }

    return satelites


# for testing purposes
if __name__ == "__main__":
    amsat = "https://www.amsat.org/tle/dailytle.txt"
    sats = fetch_tles(amsat)
    for name, data in sats.items():
        print(name)
        print(data["line1"])
        print(data["line2"])
        print()

