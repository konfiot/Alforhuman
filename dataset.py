from generateColor import generate_color_dataset
import random
import pickle as pk
import os


class Dataset:
    def __init__(self, session_id, X, y, images_path, labeled_size, labeled, unlabeled, human_pred=[], q=None):
        self.session_id = session_id
        self.X = X  # matrix format for computer
        self.images_path = images_path  # path to png images to be displayed to user
        self.y = y
        self.labeled_size = labeled_size
        self.labeled = labeled
        self.unlabeled = unlabeled
        self.q = None
        self.human_pred = human_pred
        print('labeled:', self.labeled)
        print('unlabeled:', self.unlabeled)

    def update_labeled_set(self, q):
        self.q
        assert q in self.unlabeled
        print('adding label', q)
        self.labeled_size += 1
        self.unlabeled.remove(q)
        self.labeled.append(q)
        print('labeled:', self.labeled)
        print('unlabeled:', self.unlabeled)

    def add_human_prediction(self, human_pred, q):
        self.human_pred.append((q, human_pred))

    def store(self):
        dataset_dict = {'X': self.X, 'y': self.y, 'images_path': self.images_path, 'labeled_size': self.labeled_size,
                        'labeled': self.labeled, 'unlabeled': self.unlabeled, 'human_pred': self.human_pred, 'q': self.q}
        file_path = get_dataset_file_path(self.session_id)
        with open(file_path, "wb") as f:
            pk.dump(dataset_dict, f)


# Build or load Dataset object for a session id
def generate_initial_dataset(session_id, dataset_type, dataset_path):
    print(session_id)
    if dataset_type == 'color':  # Dynamically created dataset.
        dataset_size = 20
        X, y, images_path = generate_color_dataset(dataset_path,
                                                   dataset_size=dataset_size, seed=session_id)
        labeled_size = 2
        labeled = [random.randint(0, dataset_size-1)
                   for _ in range(labeled_size)]
        unlabeled = [i for i in range(
            dataset_size) if i not in labeled]
        dataset = Dataset(session_id=session_id, X=X, y=y, images_path=images_path,
                          labeled_size=labeled_size, labeled=labeled, unlabeled=unlabeled)
        return dataset
    else:
        return NotImplementedError


# Return the dataset assigned to a particular session id
def get_dataset_of_session(session_id):
    file_path = get_dataset_file_path(session_id)
    with open(file_path, "rb") as f:
        dataset_dict = pk.load(f)

    dataset = Dataset(session_id=session_id, X=dataset_dict['X'], y=dataset_dict['y'], images_path=dataset_dict['images_path'],
                      labeled_size=dataset_dict['labeled_size'], labeled=dataset_dict['labeled'], unlabeled=dataset_dict['unlabeled'], human_pred=dataset_dict['human_pred'], q=dataset_dict['q'])
    return dataset


def get_dataset_file_path(session_id):
    path = os.path.join('session', str(session_id))
    return os.path.join(path, 'dataset.pkl')
