from src.db_connection import get_all_completed_experiment
from src.experiment import ExperimentDB
import numpy as np 

def extract_score(exp):
    pred_tuple = exp.list_human_pred_test
    num_test = len(pred_tuple)
    if num_test == 0:
        return None, None
    test_index = [i[0] for i in pred_tuple]
    pred = [i[1] for i in pred_tuple]
    y = exp.y
    ground_truth = y[test_index]
    scores = []
    for i in range(num_test):
        if pred[i] == ground_truth[i]:
            scores.append(1)
        else:
            scores.append(0) 
   
    return scores, np.mean(scores)




al_score = []
random_score = []
experiments_db = get_all_completed_experiment()
for exp_db in experiments_db:
    exp = ExperimentDB(exp_db)
    al_type = exp.al_type
    if al_type == 1:
        scores, avg_score =extract_score(exp)
        if scores is not None:
            al_score.append(avg_score)
    elif al_type == 0:
        scores, avg_score =extract_score(exp)
        if scores is not None:
            random_score.append(avg_score)
            

print('al',np.mean(al_score))
print('random',np.mean(random_score))