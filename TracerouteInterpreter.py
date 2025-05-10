import os
import datetime
import re

class TracerouteInterpreter:

# Attributes
    routeSet = []
    trcrtDates = []

# Constructors
    def __init__(self, outputPath="trcrtOutput"):
        self.outputPath = outputPath
    
# Service Methods
    def processLogs(self, filepath):
        hostName = ""
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
                            addressString += str(addresses[i]) + "," # Add each IP to a string
                addressString = addressString[0:-2]
                # The following code snippet retrieves the unix timestamp from the file name
                curFileDate = int(str(os.fsdecode(file))[-14:-4])
                curFileDate = datetime.datetime.fromtimestamp(curFileDate)
                curFileDate = [(str(curFileDate.day) + "/" + str(curFileDate.month) + "/" + str(curFileDate.year) + "~" + str(curFileDate.hour))]

                # The following code snippet checks for duplicates, only adding the route if it is not contained in self.routeSet
                addrInSet = False
                for i in range(0, len(self.routeSet)):
                    if self.routeSet[i] == addressString:
                        addrInSet = True
                        self.trcrtDates[i].append(curFileDate[0])

                if addrInSet == False:
                    self.routeSet.append(addressString)
                    self.trcrtDates.append(curFileDate)

                # The following code snippet extracts the host name for the outputLogs method
                hostName = os.fsdecode(file)[0:-15]
        self.__outputLogs(hostName)

        # Reset the attributes for further processing calls
        self.routeSet = []
        self.trcrtDates = []
                    
    def __outputLogs(self, filename="output.log"):
        outputDir = "trcrtOutput"
        filepath = self.outputPath + "/" + filename + ".log"

        if os.path.exists(self.outputPath) != True:
            os.mkdir(self.outputPath)
        # Open a new file at the specified path
        with open(filepath, "w") as f:
            # Iterate through the unique routes
            for i in range (0, len(self.routeSet)):
                curRoute = str(self.routeSet[i]) + ":"
                f.write(curRoute) # Write unique route i
                curDateList = self.trcrtDates[i]
                for j in range(0, len(curDateList)):
                    curDate = str(curDateList[j])
                    if j != len(curDateList) - 1:
                        curDate += ","
                    f.write(curDate) # Write all dates for this route
                f.write("\n")
                   
                    
                    
                    

            

                        




# Main
def main():
    myObj = TracerouteInterpreter()
    myObj.processLogs("D:/Github/Networks-Data-Interpreter/traceroute/Latvia")
    

if __name__ == "__main__":
    main()