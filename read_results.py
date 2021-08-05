import numpy as np
import matplotlib.pyplot as plt
import os
import pickle as pk



if __name__=="__main__":
    file_path = 'dataset_3.pkl'
   
    with open(file_path, "rb") as f:
        experiment = pk.load(f)
    
    print(score)