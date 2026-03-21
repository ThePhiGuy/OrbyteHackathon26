# tlefetch.py is is a library that provides functionality
# of fetching a set of TLE's from a webpage for use in other parts of the program
#
# written by Ryan Deaton (rad53@calvin.edu) for Calvin Hackathon '26 on March 2026

import requests

# utilizes a URL that points to a set of TLE's downloads them and puts them
# into a dictionary containing satelite name as the key
# and the values being line 1 and line 2 of the TLE.
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

# this function does fetch_tles for a list of urls that have TLE's
def fetch_all_tles(urls):
    sats = dict()
    for url in urls:
        sats |= fetch_tles(url) 
        # the or equals makes it so the tles will be added if they are 
        # not within, the right side of this equation overrites existing
    return sats

# for testing purposes
if __name__ == "__main__":
    amsat = "https://www.amsat.org/tle/dailytle.txt"
    sats = fetch_tles(amsat)
    for name, data in sats.items():
        print(name)
        print(data["line1"])
        print(data["line2"])
        print()

