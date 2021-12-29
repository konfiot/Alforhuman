import pymongo
import numpy as np
from pymongo import MongoClient
import pickle as pk
import os
from bson.binary import Binary
home_path = os.path.expanduser('~')

fileName = 'X509-cert-999459858208805076.pem' # CHANGE

path_to_certificate = os.path.join(home_path,'.ssh')
path_to_certificate = os.path.join(path_to_certificate,fileName)

uri = "mongodb+srv://cluster0.zdfyr.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate)


DB = client["database"]
TABLE_EXPERIMENT = 'experiment'
TABLE_DATABASE = 'database'

def store_db(collection_name, dict_entry):
    
    mycol = DB[collection_name]
    for key, val in dict_entry.items(): # check that each entry can be put in mangodb, conversion if necessary
        print(key, type(val))

        if type(val).__module__ == np.__name__: # serialize 2D array y numpy
            dict_entry[key] = Binary( pk.dumps(val, protocol=2)) 
        
    
    x = mycol.insert_one(dict_entry)
    return x.inserted_id
def get_experiment_from_db(session_id):
    experiment_table = DB[TABLE_EXPERIMENT]
    experiment_dict = [x for x in experiment_table.find({},{ "session_id": session_id})]
    print(experiment_dict)
    assert len(experiment_dict) ==1
    experiment_dict = experiment_dict[0]
    for key, val in experiment_dict.items(): # check that each entry can be put in mangodb, conversion if necessary
        print(key, type(val))
        if type(val).__module__ == Binary.__name__: 
            experiment_dict[key] =  pk.loads(val)# serialize 2D array y numpy
    return experiment_dict