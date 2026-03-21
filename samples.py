# document for methods that simulate functionality of future methods (to support frontend work)
# written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

import convertfromtle

ISSline1 = "1 25544U 98067A   26079.87218434  .00009590  00000-0  18573-3 0  9991"
ISSline2 = "2 25544  51.6346  17.0785 0006366 213.2716 146.7873 15.48402839558062"

def sampleDataList():
    list = []
    for i in range(0, 6480):
        list.append(convertfromtle.TLEtoGeodeticSecOffset(ISSline1, ISSline2, i*5))
    return list

# def fasterSampleDataList():
#     list = []
#     (convertfromtle.BatchTLEtoGeodeticSecOffset(ISSline1, ISSline2, 5, 6480))
#     return list

if __name__ == "__main__":
    print(sampleDataList())