import os
import datetime
import re

class TracerouteInterpreter:

# Attributes
    ipSet = []
    trcrtDates = []

# Constructors
    def __init__(self, outputPath="/trcrtOutput"):
        self.path = "/"
    
# Service Methods
    def processLogs(self, filepath):
        dir = os.fsencode(filepath)

        for file in os.listdir(dir):
            filename = filepath + "/" + os.fsdecode(file)
            with open(filename, "r") as curFile:
                addressString = ""

                while(True):
                    curLine = curFile.readline()

                    if curLine == "":
                        break
                    if curLine[0:10] != "traceroute": # Prevents us processing the first line and including the destination IP in our data
                        addresses = re.findall("[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}", curLine) # Extract each IP
                        for i in range (0, len(addresses)):
                            addressString += str(addresses[i]) + ", " # Add each IP to a string
                
                # The following code snippet retrieves the unix timestamp from the file name
                curFileDate = int(str(os.fsdecode(file))[-14:-4])
                curFileDate = datetime.datetime.fromtimestamp(curFileDate)
                curFileDate = [(str(curFileDate.day) + "/" + str(curFileDate.month) + "/" + str(curFileDate.year) + "~" + str(curFileDate.hour))]

                # The following code snippet checks for duplicates, only adding the route if it is not contained in self.ipSet
                addrInSet = False
                for i in range(0, len(self.ipSet)):
                    if self.ipSet[i] == addressString:
                        addrInSet = True
                        self.trcrtDates[i].append(curFileDate[0])

                if addrInSet == False:
                    self.ipSet.append(addressString)
                    self.trcrtDates.append(curFileDate)
                    


        print(self.ipSet, "\n", self.trcrtDates)

                        




# Main
def main():
    myObj = TracerouteInterpreter()
    myObj.processLogs("D:/Github/Networks-Data-Interpreter/traceroute/Latvia")
    

if __name__ == "__main__":
    main()