#from audioop import avg
from csv import reader
import os
from operator import itemgetter
from json import dumps 


## Function definition ##

## 1. Loader FUnction to read the data and convert it to Dictionary
def loader(path, header):
    with open(path) as file:
        csv_file = reader(file)
        next(csv_file)
        for row in csv_file:
            yield dict(zip(header, row))

## 2. Batch generator 
def generate_batch(data_set: list, batch_unit: int):
    for i in range(0, len(data_set), batch_unit):
        yield data_set[i : i + batch_unit]


## 3. Analytics functions, Avg, Min, Max, percentile
def calc_avg(data_set: list, key: str):
    avg = sum([float(data[key]) for data in data_set]) / len(data_set)
    #print("AVG: ", avg)
    return avg

def calc_variance(data_set: list , key: str):
    mean = calc_avg(data_set,key)
    var = sum((float(data[key]) - mean) ** 2 for data in data_set) / len(data_set)
    #print("VAR: ", var)
    return var

def find_min(data_set: list, key: str):
    _min = min(data_set, key=itemgetter(key))
    #print("Min: ", _min[key])
    return _min[key]

def find_max(data_set: list, key: str):
    _max = max(data_set, key=itemgetter(key))
    #print("Max: ", _max[key])
    return _max[key]

def calc_percentile(data_set: list, key: str, percentage: float):
    sorted_data = sorted([float(data[key]) for data in data_set])
    _max = max(sorted_data) 
    percentage = _max * (percentage / 100) 
    start_point = _max - percentage
    # result = [value for value in sorted_data 
    #           if value >= start_point]
    return start_point

   
   
HEADERS = ("cpu_utilization_average", "network_in_average",
               "network_out_average", "memory_utilization_average", "final_target")
absolute_dir = os.getcwd() 
DATA_SET_MAPPING = {
    "dvd_testing": list(loader(absolute_dir +  r"/Dataset/DVD-testing.csv",HEADERS)),
    "dvd_training": list(loader(absolute_dir +  r"/Dataset/DVD-training.csv",HEADERS)) ,
    "ndbench_testing": list(loader(absolute_dir +  r"/Dataset/NDBench-testing.csv",HEADERS)),
    "ndbench_training": list(loader(absolute_dir +  r"/Dataset/NDBench-training.csv",HEADERS))
}


# calc_avg(DATA_SET_MAPPING["ndbench_test"], "network_in_average")
# find_min(DATA_SET_MAPPING["ndbench_test"], "network_in_average")
# find_max(DATA_SET_MAPPING["ndbench_test"], "network_in_average")
# result = calc_percentile(DATA_SET_MAPPING["ndbench_test"][0:99], "network_in_average", 1)
# print(result)
# print(dumps({"percentile_result": result}))
# print(DATA_SET_MAPPING["dvd_test"])
# batch_400 = []
# batch_400 = generate_batch(DATA_SET_MAPPING["ndbench_test"],10)
# for x in batch_400:
#     print(x)
#print(len(DATA_SET_MAPPING['ndbench_training']))

if __name__ == "__main__":
    pass
   