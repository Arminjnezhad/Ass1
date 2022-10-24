import pickle

#Serialization and Deserialization
# A test object
test_dict = {"Hello": "World!"}
 
# Serialization
with open("test.pickle", "wb") as outfile:
    pickle.dump(test_dict, outfile)
print("Written object", test_dict)
 
# Deserialization
with open("test.pickle", "rb") as infile:
    test_dict_reconstructed = pickle.load(infile)
print("Reconstructed object", test_dict_reconstructed)
 
if test_dict == test_dict_reconstructed:
    print("Reconstruction success")