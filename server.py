# Importing the required libraries
import socket
import re
import json
from datetime import datetime
import os
from _thread import *
import dataToJSON

# Defining the required functions:
def dataManipulation(req):
    rfwID = req["rfwID"]
    dataset_name = req["benchmark"] + "_" + req["dataType"] 
    metric = req["workloadMetric"]
    batchUnit = req["batchUnit"]
    batchID = req["batchID"]
    batchSize = req["batchSize"]
    dataAnalysisType = req["dataAnalysis"]

    if req["workloadMetric"] == 'cpu':
        metric = dataToJSON.HEADERS[0]
    elif req["workloadMetric"] == 'networkin':
        metric = dataToJSON.HEADERS[1]
    elif req["workloadMetric"] == 'networkout':
        metric = dataToJSON.HEADERS[2]
    elif req["workloadMetric"] == 'memory':
        metric = dataToJSON.HEADERS[3]

    result = {}
    result["rfwID"] = rfwID
    batch_list = list(dataToJSON.generate_batch(dataToJSON.DATA_SET_MAPPING[dataset_name], batchUnit))

    if batchID > len(batch_list) or (batchID + batchSize) > len(batch_list):
        result["error"] = "The batch ID or the number of request batches are is bigger than the length of all batches!!!"
    else:
        result["lastBatchID"] = batchID + batchSize
        reqestedData = batch_list[batchID:batchID+batchSize]
        result["dataRequested"] = reqestedData
        result["analysis"] = {}
        dataset = [j for i in batch_list for j in i] #For calculation
        result["analysis"][metric] = {}
        for method in dataAnalysisType:
            if re.match('p\d+',method):
                precent = int(re.search("\d+", method).group())
                result["analysis"][metric][method]=dataToJSON.calc_percentile(dataset ,metric, precent)
            elif method=="avg":
                result["analysis"][metric][method]=dataToJSON.calc_avg(dataset ,metric)
            elif method=="std":
                result["analysis"][metric][method]=dataToJSON.calc_variance(dataset, metric)
            elif method=="max":
                result["analysis"][metric][method]=dataToJSON.find_max(dataset ,metric)
            elif method=="min":
                result["analysis"][metric][method]=dataToJSON.find_min(dataset ,metric)
    return result

#### 

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0

## Defining the required function
def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        clientRequest = data.decode('utf-8')
        print("Client Request:\n", clientRequest)
        clientRequest = json.loads(clientRequest)
        #print(clientRequest)
        response = dataManipulation(clientRequest)
        #print(response)
        response = json.dumps(response)
        #response = "This message is from Server, " + datetime.now().strftime("%c") + '\n' + response
        # response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))
    connection.close()
##

## Listening to the clients
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

## Accepting client socket connection
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()