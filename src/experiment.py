from src.generateColor import get_next_dataset 
import random
import pickle as pk
import os

DYNAMIC_DATASET = ['color']

class Experiment:
    def __init__(self, session_id, al_type, X, y, images_path, init_labeled_size, labeled, unlabeled):
        self.session_id = session_id
        self.al_type = al_type
        self.X = X  # matrix format for computer
        self.images_path = images_path  # path to png images to be displayed to user
        self.y = y # list of labels
        self.init_labeled_size = init_labeled_size # size of the label set showed at the beginning
        self.labeled = labeled # list of labeled_index
        self.labeled_size  = len(self.labeled)
        self.unlabeled = unlabeled # list of unlabeled_index
        self.test_indices = unlabeled
        self.list_human_pred_test = [] # list of tuple  (index, human label pred)
        self.list_human_pred_train = [] # list of tuple  (index, human label pred)
        self.test_index = 0 # keep track of which test images has been shown for server version
        self.experiment_completed = False

    def update_labeled_set(self, q):
        self.q = q
        assert q in self.unlabeled
        self.labeled_size += 1
        self.unlabeled.remove(q)
        self.labeled.append(q)
        self.test_indices = self.unlabeled

    def add_human_prediction(self, human_pred, q): # add prediction of human during the training phase (the feedback is given)
        self.list_human_pred_train.append((q, human_pred))

    def add_test_human_pred(self, human_pred_test, q): # add prediction at test time
        self.list_human_pred_test.append((q, human_pred_test))
    
    def set_experiment_completed(self):
        self.experiment_completed = True
        
    def increment_test_index(self):
        self.test_index = self.test_index+1

    def store(self):
        file_path = get_dataset_file_path(self.session_id)
        print('label',self.labeled)
        print('labeled_size',self.labeled_size)
        print('unlabeled',self.unlabeled)
        print('test_indices',self.test_indices)
        print('list_human_pred_test',self.list_human_pred_test)
        print('list_human_pred_train',self.list_human_pred_train)
        print('test_index',self.test_index)
        print('----------------')
        with open(file_path, "wb") as f:
            pk.dump(self, f)
    



# Build experiment object for a session id. dataset_path unusued for now
def link_dataset_to_session(session_id, dataset_type, al_type, dataset_path):
    if dataset_type == 'color': 
        init_labeled_size = 3
        X,y,images_path = get_next_dataset()
        dataset_size = len(images_path)
       
        labeled = [random.randint(0, dataset_size-1)
                   for _ in range(init_labeled_size)]
        unlabeled = [i for i in range(
            dataset_size) if i not in labeled]
        experiment = Experiment(session_id=session_id, al_type=al_type, X=X, y=y, images_path=images_path,
                          init_labeled_size=init_labeled_size, labeled=labeled, unlabeled=unlabeled)
        return experiment
    else:
        return NotImplementedError

# Return the dataset assigned to a particular session id
def get_experiment_of_session(session_id):
    file_path = get_dataset_file_path(session_id)
    with open(file_path, "rb") as f:
        experiment = pk.load(f)
    return experiment

def get_dataset_file_path(session_id):
    path = os.path.join('session', str(session_id))
    return os.path.join(path, 'dataset.pkl')


