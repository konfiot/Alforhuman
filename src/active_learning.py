
import random
from modAL.models import ActiveLearner
from sklearn.ensemble import RandomForestClassifier

def generate_next_query(experiment):
    al_type = experiment.al_type
    if al_type == 0 :
        q = random.choice(experiment.unlabeled)
    elif al_type == 1:
        X_training = experiment.X[experiment.labeled, :] 
        y_training = experiment.y[experiment.labeled]
        X_pool = experiment.X[experiment.unlabeled, :] 
       
        # initializing the learner
        learner = ActiveLearner(
            estimator=RandomForestClassifier(),
            X_training=X_training, y_training=y_training
        )
        
        query_idx, _ = learner.query(X_pool)
        q = experiment.unlabeled[query_idx[0]]
        print(q)
    experiment.update_labeled_set(q)
    return q

    
