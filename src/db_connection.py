import pymongo
import numpy as np
from pymongo import MongoClient
import pickle as pk
import os
from bson.binary import Binary
home_path = os.path.expanduser('~')

fileName = 'X509-cert-999459858208805076.pem' # CHANGE

if os.getenv('MONGODB_CERT'):
    with open(filename, 'w') as f:
        f.write(os.getenv("MONGODB_CERT"))

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
    col = DB[collection_name]
    x = col.insert_one(dict_entry)
    return x.inserted_id
def get_experiment_from_db(session_id):
    experiment_table = DB[TABLE_EXPERIMENT]
    myquery = {"session_id": session_id}
    experiment_dict = experiment_table.find_one(myquery)
    #TODO add checkhere that experiment_dict is not empty
    
   
    return experiment_dict

def update_experiment_db_entry(session_id, updated_dict):
    col = DB[TABLE_EXPERIMENT]
    myquery = {"session_id":session_id}
    newvalues = { "$set": updated_dict }

    col.update_one(myquery, newvalues)
