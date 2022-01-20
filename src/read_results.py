import numpy as np
import matplotlib.pyplot as plt
import os
import pickle as pk



if __name__=="__main__":
    file_path = 'dataset_3.pkl'
   
    with open(file_path, "rb") as f:
        experiment = pk.load(f)
    
    print(experiment.experiment_completed)
    print(experiment.list_human_pred_train)
    print(experiment.list_human_pred_test)