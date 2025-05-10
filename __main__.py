'''
* Networks Data Interpreter (CMP-5037B-24)
    Author: Sunny Ledger
    Date: 06/05/2025
    Description: Networks Data Interpreter is a relatively straightforward
'''

import datetime
from PingInterpreter import PingInterpreter
from TracerouteInterpreter import TracerouteInterpreter


def main():
    #pingObj = PingInterpreter("D:/Github/Networks-Data-Interpreter/ping/data", datetime.datetime(2025, 5, 1), "test.csv")
    #pingObj.processData()

    trcrtObj = TracerouteInterpreter()

    filepathNames = ["Latvia", "Luxembourg", "NewZealand", "Poland", "SouthAfrica", "Taiwan", "UK", "USA"]
    for directory in filepathNames:
        curFilepath = "D:/Github/Networks-Data-Interpreter/traceroute/" + directory
        trcrtObj.processLogs(curFilepath)

if __name__ == "__main__":
    main()