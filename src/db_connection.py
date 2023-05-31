import pymongo
import numpy as np
from pymongo import MongoClient
import pickle as pk
import os
from bson.binary import Binary

home_path = os.path.expanduser('~')

TABLE_EXPERIMENT = 'experiment'
TABLE_DATABASE = 'database'
TABLE_MUSHROOM_DATABASE = 'mushroom_database'

fileName = 'X509-cert-5983501895474278860.pem' # CHANGE


path_to_certificate = os.path.join(home_path,'.ssh')
try:
    os.mkdir(path_to_certificate)
except OSError as error:
    print(error)    
path_to_certificate = os.path.join(path_to_certificate,fileName)

if os.getenv('MONGODB_CERT', None):
    print('loading from MONGODB_CERT...')
    with open(path_to_certificate, 'w') as f:
        f.write(os.getenv("MONGODB_CERT", None))
        print("file written")
else:
    
    print(os.getenv("MONGODB_CERT", None))


uri = "mongodb+srv://cluster0.zdfyr.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate)


DB = client["database"]
def store_db(collection_name, dict_entry):
    col = DB[collection_name]
    x = col.insert_one(dict_entry)
    return x.inserted_id
    
def store_db_or_get_id(collection_name,dict_entries):
    col = DB[collection_name]
    if col.count_documents({"type":"mushroom"}) == 0:
        for dict_entry in dict_entries:
            x = col.insert_one(dict_entry)
    
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


def get_all_completed_experiment():
    experiment_table = DB[TABLE_EXPERIMENT]
    myquery = {"experiment_completed": True}
    experiment_dict = experiment_table.find(myquery)
    return experiment_dict
