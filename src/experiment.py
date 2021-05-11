from src.generateColor import generate_color_dataset
import random
import pickle as pk
import os

DYNAMIC_DATASET = ['color']

class Experiment:
    def __init__(self, session_id, al_type, X, y, images_path, labeled_size, labeled, unlabeled, human_pred=[], q=None, score=None):
        self.session_id = session_id
        self.al_type = al_type
        self.X = X  # matrix format for computer
        self.images_path = images_path  # path to png images to be displayed to user
        self.y = y
        self.labeled_size = labeled_size
        self.labeled = labeled
        self.unlabeled = unlabeled
        self.q = q
        self.human_pred = human_pred
        self.test_indices = unlabeled
        self.score = score
     

    def update_labeled_set(self, q):
        self.q
        assert q in self.unlabeled
        self.labeled_size += 1
        self.unlabeled.remove(q)
        self.labeled.append(q)
        self.test_indices = self.unlabeled

    def add_human_prediction(self, human_pred, q):
        self.human_pred.append((q, human_pred))

    def set_score(self, score):
        self.score = score

    def store(self):
        file_path = get_dataset_file_path(self.session_id)
        with open(file_path, "wb") as f:
            pk.dump(self, f)


# Build or load experiment object for a session id
def generate_initial_dataset(session_id, dataset_type, data_path, al_type):
    if dataset_type == 'color':  # Dynamically created dataset.
        dataset_size = 20
        seed = session_id
        dataset_path = get_image_file_path(data_path, dataset_type, seed)
        
        X, y, images_path = generate_color_dataset(dataset_path,
                                                   dataset_size=dataset_size, seed=seed)
        labeled_size = 2
        labeled = [random.randint(0, dataset_size-1)
                   for _ in range(labeled_size)]
        unlabeled = [i for i in range(
            dataset_size) if i not in labeled]
        experiment = Experiment(session_id=session_id, al_type=al_type, X=X, y=y, images_path=images_path,
                          labeled_size=labeled_size, labeled=labeled, unlabeled=unlabeled)
        return experiment
    else:
        return NotImplementedError

# Return the dataset assigned to a particular session id
def get_experiment_of_session(session_id):
    file_path = get_dataset_file_path(session_id)
    with open(file_path, "rb") as f:
        experiment = pk.load(f)
    return experiment

def get_image_file_path(data_path, dataset_type, seed):
    dataset_name_path = dataset_type+'_'+str(seed)
    dataset_path = os.path.join(data_path, dataset_name_path)
    return dataset_path

def get_dataset_file_path(session_id):
    path = os.path.join('session', str(session_id))
    return os.path.join(path, 'dataset.pkl')


