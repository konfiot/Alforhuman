import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import os


def store_image_return_path(x,file_path):
    A = np.zeros((100, 100, 3))
    A[:, :, :] = x/255
    plt.imshow(A)
    plt.savefig(file_path)
    plt.close()

def show_image(file_path, label=None):
    A = np.zeros((100, 100, 3))

    A[:, :, :] = x/255
    plt.imshow(A)
    if label is None:
        plt.title('What is this ?')
    else:
        plt.title('This is '+str(label))
    plt.show()
    plt.close()


def assign_binary_label(color, decision_func):
    if decision_func(color) < 0:
        return 1
    else:
        return 0


def generate_color_dataset(dataset_path, dataset_size, seed):

    color_corner_a = [0, 130, 221]
    color_corner_b = [134, 0, 13]
  
    reds = [random.randint(color_corner_a[0], color_corner_b[0])
            for _ in range(dataset_size)]
    blues = [random.randint(color_corner_b[1], color_corner_a[1])
             for _ in range(dataset_size)]
    greens = [random.randint(color_corner_b[2], color_corner_a[2])
              for _ in range(dataset_size)]

    def decision_func(color):
        r = np.abs(color_corner_b[0]-color_corner_a[0])
        g = np.abs(color_corner_b[1]-color_corner_a[1])
        b = np.abs(color_corner_b[2]-color_corner_a[2])
        if color[0] < r:
            return -1
        else:
            return 1

    y = []
    for i in range(dataset_size):
        color = [reds[i], blues[i], greens[i]]
        y.append(assign_binary_label(color, decision_func))
    X = np.zeros((dataset_size, 3))
    X[:, 0] = reds
    X[:, 1] = blues
    X[:, 2] = greens
    y = np.array(y)

    # Now we create a folder for the dataset and store the images
    dataset_name_path = 'color_'+str(seed)
    dataset_path = os.path.join('datasets',dataset_name_path)
    os.makedirs(dataset_path)
    # store all files and append list of paths
    images_path = []
    for i in range(dataset_size):
        filename = str(i)+'.png'
        file_path = os.path.join(dataset_path, filename)
        store_image_return_path(X[i,:],file_path)
        images_path.append(file_path)
        
    return X, y,images_path


if __name__ == '__main__':
    X, y = generate_dataset(50)
    
    for i in range(50):
        show_image(X[i, :], y[i])
