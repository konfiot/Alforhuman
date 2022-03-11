from src.db_connection import get_all_completed_experiment
from src.experiment import ExperimentDB
import numpy as np 
from scipy.stats import fisher_exact, ttest_ind


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




al_scores = []
random_scores = []
experiments_db = get_all_completed_experiment()
for exp_db in experiments_db:
    exp = ExperimentDB(exp_db)
    al_type = exp.al_type
    if al_type == 1:
        scores, avg_score =extract_score(exp)
        if scores is not None:
            al_scores.append(scores)
    elif al_type == 0:
        scores, avg_score =extract_score(exp)
        if scores is not None:
            random_scores.append(scores)
            
means_al = [np.mean(i) for i in al_scores]
means_rd = [np.mean(i) for i in random_scores]

print('AL Experiment Result...')
print()
print("Total trials", len(means_al)+len(means_rd))
print('Mean accuracy with al :',np.mean(means_al))
print('Mean accuracy with random :',np.mean(means_rd))
stat, p_val = ttest_ind(means_al, means_rd)
print()
if p_val < 0.05:
    print('with significane')
else:
    print('without significance')
