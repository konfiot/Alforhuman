
import random
from modAL.models import ActiveLearner
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

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
            estimator=AdaBoostClassifier(),
            X_training=X_training, y_training=y_training
        )
        
        query_idx, _ = learner.query(X_pool)
        q = experiment.unlabeled[query_idx[0]]
    elif al_type == 2:
        X_training = experiment.X[experiment.labeled, :] 
        y_training = experiment.y[experiment.labeled]
        X_pool = experiment.X[experiment.unlabeled, :] 
        if len(experiment.list_human_pred_train) > 0:
           
            y_training = y_training[:experiment.init_labeled_size] + [human_tuple[1] for human_tuple in experiment.list_human_pred_train]
        # initializing the learner
        learner = ActiveLearner(
            estimator=AdaBoostClassifier(),
            X_training=X_training, y_training=y_training
        )
        query_idx, _ = learner.query(X_pool)
        q = experiment.unlabeled[query_idx[0]]
    experiment.update_labeled_set(q)
    return q

    
