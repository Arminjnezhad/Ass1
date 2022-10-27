# Importing the required libraries 
import socket
import json
from datetime import datetime
import re

# Defining the required functions:
def requestMessage():
    # 1. RFW ID
    # 2. Benchmark Type (such as DVD store or NDBench)
    # 3. Workload Metric (such as CPU or NetworkIn or NetworkOut or
    # Memory)
    # 4. Batch Unit (the number of samples contained in each batch, such
    # as 100)
    # 5. Batch ID (such as the 1st or 2nd or… 5th Batch)
    # 6. Batch Size (such as the how many batches to return, 5 means 5
    # batches to return)
    # 7. Data Type (training data or testing data)
    # 8. Data analytics ( 10p, 50p, 95p, 99p, avg, std, max, min), for
    # example 50p means 50th percentile
    rfw=dict()

    print("It is required some more steps before sending your request...")

    rfwID = input("Specify the RFW ID: ")
    while not rfwID.isdigit():
        print("You inserted the wrong value...")
        rfwID = input("Specify the RFW ID: ")
    rfw["rfwID"] = int(rfwID)

    benchmark = input("Specify the benchmark type (DVD or NDBench): ").lower()
    while benchmark!='dvd' and benchmark!='ndbench':
        print("You inserted the wrong value...")
        benchmark = input("Specify the benchmark type (DVD or NDBench): ").lower()
    rfw["benchmark"] = benchmark

    metric = input("Specify the workload metric (CPU or NetworkIn or NetworkOut or Memory):").lower()
    while metric not in ['cpu', 'networkin', 'networkout', 'memory']:
         print("You inserted the wrong value...")
         metric = input("Specify the workload metric (CPU or NetworkIn or NetworkOut or Memory):").lower()
    rfw["workloadMetric"] = metric

    batchUnit = input("Specify the batch unit number: ")
    while not batchUnit.isdigit():
        print("You inserted the wrong value...")
        batchUnit = input("Specify the batch unit number: ")
    rfw["batchUnit"] = int(batchUnit)
        
    batchID = input("Specify the batch ID: ")
    while not batchID.isdigit():
        print("You inserted the wrong value...")
        batchID = input("Specify the batch ID: ")
    rfw["batchID"] = int(batchID)

    batchSize = input("Specify the batch size: ")
    while not batchSize.isdigit():
        print("You inserted the wrong value...")
        batchSize = input("Specify the batch size: ")
    rfw["batchSize"] = int(batchSize)

    dataType = input("Specify the data type (training or testing): ").lower()
    while dataType!='training' and dataType!='testing':
        print("You inserted the wrong value...")
        dataType = input("Specify the data type (training or testing): ").lower()
    rfw["dataType"] = dataType

    dataAnalysis = []
    print("Speicfy the desired data analytics (10p, 50p, 95p, 99p, avg, std, max, min).")    
    for item in ["p10", "p50", "p95", "p99", "avg", "std", "max", "min"]:
        temp=input("Do you want to calcualte " + item + " Y/N? ").lower()
        while temp not in ['y', 'n']:
            print("Please only enter Y or N.")
            temp=input("Do you want to calcualte " + item + " Y/N? ").lower()
        if temp == 'y':
            dataAnalysis.append(item)
    rfw["dataAnalysis"] = dataAnalysis


    return rfw
##


ClientMultiSocket = socket.socket()
host = '44.210.137.222'
port = 2004
print('*******************************')
print("************Welcome************")
print('*******************************')
print('Waiting for connection response')
# Initialization of counter
count = 0

# Trying to connect to the server
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)

#requestMessage()
 
# Sending the data
while True:
    #userInput = input('Hey there: ')
    count += 1
    userInput = requestMessage()
    userInput = json.dumps(userInput)
    ClientMultiSocket.send(str.encode(userInput))

    dt = datetime.now()
    res = ClientMultiSocket.recv(1024000)
    serverResponse = res.decode('utf-8')
    serverResponse = json.loads(serverResponse)
    #print(serverResponse)
    dt = datetime.now()
    with open('RFD_' + dt.strftime("%b%d_%H%M%S") + '_' + str(count) + '.txt', 'w') as f:
        f.write(json.dumps(serverResponse, indent=4))
        print("File is saved...\n\n")
ClientMultiSocket.close()