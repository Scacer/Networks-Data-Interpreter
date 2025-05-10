import os
import datetime

class PingInterpreter:
    
# Attributes
    pingData = [] # Will hold the final data to be written to a file
    processMessages = [] # Will hold any messages to be output into a log

# Constructors

    # This constructor takes an argument for filepath, startDate. If left empty, default values are the current working directory, and today's date respectively.
    def __init__(self, directory=os.getcwd(), startDate=datetime.datetime.now().date(), filename="pingOutput.csv"):
        self.filepath = directory
        self.pingData.append(["Host", "Date", "Time", "Packet Loss", "min", "avg", "max", "mdev"])
        self.startDate = startDate
        self.outputName = filename

# Service Methods
    def processData(self):
        directory = os.fsencode(self.filepath)

        for file in os.listdir(directory):   
            filename = os.fsdecode(file)

            if filename.endswith(".log"): # if a log file is found, process it
                self.__processFile(filename) 
            else: # if a non-log file is found, keep track of it with a message in self.processMessage
                self.processMessages.append("File with name: \"" + filename + "\" was found, but not identified as a log file.")
                self.processMessages.append("!--> Ensure all log files have filenames ending in \".log\"")
        
        self.__writeData() # Once data has been collected, write it to output files
    
# Support Methods
    # processFile
    #   - Processes the ping data within a specific file
    def __processFile(self, filename):

        filepath = self.filepath + "/" + filename

        # counter keeps track of which line we are on
        counter = 1
        # day keeps track of how many days have elapsed for each data point
        day = 0
        localData = []

        with open(filepath, "r") as f: # Close the file after exiting this scope
            
            while(True):
                curLine = f.readline()
                if curLine == "": # detect the end of a file
                    break # breaks the loop where there is no next line
                elif counter % 2 == 1:
                    localData.append(curLine[-30:-28]) # Extract the packet loss data from the first line
                elif counter % 2 == 0:
                    text = (curLine.removeprefix("rtt min/avg/max/mdev = ")[:-4]).split('/') # Extract the rtt data from the second line
                    for field in text: # place all of the rtt data in the localData array
                        localData.append(field)
                    packagedData = self.__packageData(localData, filename, day) # send localData to be packaged, returning the packaged data
                    self.pingData.append(packagedData) # add the packaged data to self.pingData array
                    localData = [] # reset local data
                    day += 1 # increment number of days elapsed
                    

                counter += 1
        # Close the file after exiting this scope

    # packageData
    #   - Packages data into an array appropriate for the headers set in self.pingData during instantiation
    def __packageData(self, data, filename, day):

        # Prepare semantic information
        outputDate = (self.startDate + datetime.timedelta(days=day))
        dataArray = [filename[:-7], str(outputDate.date()), filename[-6:-4] + ":00"]

        # Add each datapoint from the data argument to the entry
        for dataPoint in data:
            dataArray.append(dataPoint)
        # Return the data entry, to be added to self.pingData elsewhere
        return dataArray 
    
    # writeData
    #   - Writes data held in self.pingData to an output file, the name of which is determined by self.outputName
    def __writeData(self):

        with open(self.outputName, "w") as f: # this scope writes self.pingData to an output file
            for data in self.pingData:
                f.write(data[0] + ", " + data[1] + ", " + data[2] + ", " + data[3] + ", " + data[4] + ", " + data[5] + ", " + data[6] + "\n")
        
        if len(self.processMessages) > 0: # this condition checks for any process messages
            with open("messages.txt") as f: # this scope writes self.processMessages to an output file
                for data in self.processMessages:
                    f.write(data + "\n")
            self.processMessages.clear() # prevents duplicate messages being output on secondary call of writeData()
        


       


def main():
    myObj = PingInterpreter("D:/Github/Networks-Data-Interpreter/ping/data", datetime.datetime(2025, 5, 1), "test.csv")
    myObj.processData()

if __name__ == "__main__":
    main()
