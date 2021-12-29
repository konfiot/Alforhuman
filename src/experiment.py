from src.generateColor import get_next_dataset
from src.db_connection import store_db, get_experiment_from_db, TABLE_EXPERIMENT, TABLE_DATABASE
import random
import time
import pickle as pk
import os

DYNAMIC_DATASET = ['color']


class Experiment:
    def __init__(self, session_id, al_type, X, y, images_path, init_labeled_size, labeled, unlabeled):
        self.session_id = session_id
        self.al_type = al_type
        self.X = X  # matrix format for computer
        self.images_path = images_path  # path to png images to be displayed to user
        self.y = y  # list of labels
        # size of the label set showed at the beginning
        self.init_labeled_size = init_labeled_size
        self.labeled = labeled  # list of labeled_index
        self.labeled_size = len(self.labeled)
        self.unlabeled = unlabeled  # list of unlabeled_index
        self.test_indices = unlabeled
        # list of tuple  (index, human label pred)
        self.list_human_pred_test = []
        # list of tuple  (index, human label pred)
        self.list_human_pred_train = []
        self.test_index = 0  # keep track of which test images has been shown for server version
        self.experiment_completed = False

    def update_labeled_set(self, q):
        self.q = q
        assert q in self.unlabeled
        self.labeled_size += 1
        self.unlabeled.remove(q)
        self.labeled.append(q)
        self.test_indices = self.unlabeled

    # add prediction of human during the training phase (the feedback is given)
    def add_human_prediction(self, human_pred, q):
        self.list_human_pred_train.append((q, human_pred))

    def add_test_human_pred(self, human_pred_test, q):  # add prediction at test time
        self.list_human_pred_test.append((q, human_pred_test))

    def set_experiment_completed(self):
        self.experiment_completed = True

    def increment_test_index(self):
        self.test_index = self.test_index+1
    def get_db_entry(self):
        experiment_entry = self.__dict__
        return experiment_entry 
    def store(self, db):
        if db:
            return NotImplementedError
            # TODO get database from db
        else:
            file_path = get_dataset_file_path(self.session_id)
            with open(file_path, "wb") as f:
                pk.dump(self, f)
        print('label', self.labeled)
        print('labeled_size', self.labeled_size)
        print('unlabeled', self.unlabeled)
        print('test_indices', self.test_indices)
        print('list_human_pred_test', self.list_human_pred_test)
        print('list_human_pred_train', self.list_human_pred_train)
        print('test_index', self.test_index)
        print('----------------')

class ExperimentDB(Experiment):
    def __init__(self, dict1):
        self.__dict__.update(dict1)

# Build experiment object for a session id. dataset_path unusued for now
def link_dataset_to_session(session_id, dataset_type, al_type, dataset_path, db):
    if dataset_type == 'color':
        init_labeled_size = 3
        X, y, images_path = get_next_dataset()
        dataset_size = len(images_path)
        labeled = random.sample(range(dataset_size), init_labeled_size)
        unlabeled = [i for i in range(
            dataset_size) if i not in labeled]
        experiment = Experiment(session_id=session_id, al_type=al_type, X=X, y=y, images_path=images_path,
                                init_labeled_size=init_labeled_size, labeled=labeled, unlabeled=unlabeled)
        
        if db:
            database_entry = {'type':dataset_type, 'X':X, 'y':y, 'size':dataset_size }
            db_id = store_db(collection_name=TABLE_DATABASE,dict_entry=database_entry)
            experiment_entry = experiment.get_db_entry()
            experiment_entry['db_id'] = db_id
            store_db(collection_name=TABLE_EXPERIMENT,dict_entry=experiment_entry)
        return experiment
    else:
        return NotImplementedError

# Return the dataset assigned to a particular session id

def get_experiment_of_session(session_id, db):
    if db:
        experiment_dict = get_experiment_from_db(session_id)
        experiment = ExperimentDB(experiment_dict)
        return experiment
    else:
        file_path = get_dataset_file_path(session_id)
        with open(file_path, "rb") as f:
            experiment = pk.load(f)
        return experiment


def get_dataset_file_path(session_id):
    path = os.path.join('session', str(session_id))
    return os.path.join(path, 'dataset.pkl')
