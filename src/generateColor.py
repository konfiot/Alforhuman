import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import os
import time
import pickle as pk


data_path = 'static/data'
counter_file = os.path.join(data_path, "dataset_counter.txt")


def store_image_return_path(x, file_path):
    A = np.zeros((100, 100, 3))
    A[:, :, :] = x
    plt.imshow(A)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


def show_image(x, label=None):
    A = np.zeros((100, 100, 3))
    A[:, :, :] = x
    plt.ion()
    plt.axis('off')
    plt.show()
    plt.imshow(A)

    if label is None:
        plt.title('What is this ?')
    else:
        plt.title('This is '+str(label))
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)
    plt.close()


def show_dataset(A):
    plt.imshow(A)
    plt.axis('off')
    plt.show()
    plt.close()


def generate_color_dataset(dataset_path, dataset_size, seed):
    A = create_color_task(seed)
    show_dataset(A)
    max_step = A.shape[0]
    X = np.zeros((dataset_size, 3))
    y = []
    for i in range(dataset_size):
        index_x = random.randint(0, max_step-1)
        index_y = random.randint(0, max_step-1)
        X[i, :] = A[index_x, index_y, :]
        if index_x+index_y < max_step:
            label = 0
        else:
            label = 1
        y.append(label)
    y = np.array(y)

    # Now we create a folder for the dataset and store the images

    os.makedirs(dataset_path, exist_ok=True)
    # store all files and append list of paths

    images_path = []
    for i in range(dataset_size):
        filename = str(i)+'.png'
        file_path = os.path.join(dataset_path, filename)
        store_image_return_path(X[i, :], file_path)
        images_path.append(file_path)

    return X, y, images_path


COLOR_MAX = 255


def generate_random_color(bias=None):
    blue = random.randint(0, COLOR_MAX)/COLOR_MAX
    red = random.randint(0, COLOR_MAX)/COLOR_MAX
    green = random.randint(0, COLOR_MAX)/COLOR_MAX

    if bias == 'blue':
        blue = 1
        red = 0.1
    if bias == 'red':  # orange
        red = 1
        green = 0.2
        blue = 0
    if bias == 'green':
        green = 1
        blue = 0.1
    return np.array([red, green, blue])


def get_color_matrix(colorfrom, colorto):
    steps = 100
    A = np.zeros((steps, steps, 3))
    for i in range(steps):
        for j in range(steps):
            scale = (i+j)/(2*steps)
            A[i, j, :] = colorfrom + (colorto - colorfrom)*scale
    return A


def create_color_task(seed):
    # generate three random colors, that are different enough
    random.seed(seed)
    color1 = generate_random_color()
    rgb_color_1 = color1/np.linalg.norm(color1)
    l2_color_diff = 0
    while l2_color_diff < 0.7:  # make sure the task is not too hard, the difference between the two colors has to be big enough
        color2 = generate_random_color()
        A = get_color_matrix(color1, color2)
        rgb_color_2 = color2/np.linalg.norm(color2)
        l2_color_diff = np.linalg.norm(rgb_color_1-rgb_color_2)

    return A


def get_image_file_path(data_path, dataset_type, seed):
    dataset_name_path = dataset_type+'_'+str(seed)
    dataset_path = os.path.join(data_path, dataset_name_path)
    return dataset_path


def get_next_dataset():
    counter_file
    f = open(counter_file, "r")
    last_seed = int(f.read())

    dataset_path = get_image_file_path(
        data_path, dataset_type='color', seed=last_seed)
    data_file_path = os.path.join(dataset_path, 'data.pkl')

    with open(data_file_path, "rb") as f:
        dataset_data = pk.load(f)
    with open(counter_file, "w") as f:
        f.write(str(last_seed+1))

    return dataset_data['X'], dataset_data['y'], dataset_data['images_path']


# Generate bunch of datasets. created in data_path, create the counter file.
if __name__ == '__main__':

    if not os.path.exists(data_path):
        print('Creating the dataset folder since it wasn\'t there\n')
        os.makedirs(data_path)

    NUM_DATASETS = 10
    dataset_size = 30
    start_seed = int(time.time() * 10000000)  # This should always increase

    with open(counter_file, "w") as f:
        f.write(str(start_seed))

    for i in range(NUM_DATASETS):
        print('Generating dataset', i+1, '/', NUM_DATASETS)
        seed = start_seed + i
        dataset_path = get_image_file_path(
            data_path, dataset_type='color', seed=seed)

        X, y, images_path = generate_color_dataset(dataset_path,
                                                   dataset_size=dataset_size, seed=seed)
        dataset_data = {'X': X, 'y': y, 'images_path': images_path}
        data_file_path = os.path.join(dataset_path, 'data.pkl')
        with open(data_file_path, "wb") as f:
            pk.dump(dataset_data, f)
