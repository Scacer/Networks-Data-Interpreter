'''
* Networks Data Interpreter (CMP-5037B-24)
    Author: Sunny Ledger
    Date: 06/05/2025
    Description: Networks Data Interpreter is a relatively straightforward
'''
import datetime
from PingInterpreter import PingInterpreter


def main():
    myObj = PingInterpreter("D:/Github/Networks-Data-Interpreter/ping/data", datetime.datetime(2025, 5, 1), "test.csv")
    myObj.processData()

if __name__ == "__main__":
    main()