import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import os


def store_image_return_path(x, file_path):
    A = np.zeros((100, 100, 3))
    A[:, :, :] = x
    plt.imshow(A)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


def show_image(x, label=None):
    A = np.zeros((100, 100, 3))
    A[:, :, :] = x
    plt.ion()
    plt.show()
    plt.imshow(A)
    
    if label is None:
        plt.title('What is this ?')
    else:
        plt.title('This is '+str(label))
    plt.tight_layout()
    plt.draw()
    plt.pause(2)
    plt.close()


def show_dataset(A):
    plt.imshow(A)
    plt.show()
    plt.close()

def generate_color_dataset(dataset_path, dataset_size, seed):
    A = create_color_task(seed)
    #show_dataset(A)
    max_step = A.shape[0]
    X = np.zeros((dataset_size, 3))
    y = []
    for i in range(dataset_size):
        index_x = random.randint(0,max_step-1)
        index_y = random.randint(0,max_step-1)
        X[i,:] = A[index_x,index_y,:]
        if index_x+index_y < max_step:
            label=0
        else:
            label=1
        y.append(label)
    y = np.array(y)

    # Now we create a folder for the dataset and store the images
    dataset_name_path = 'color_'+str(seed)
    dataset_path = os.path.join('datasets', dataset_name_path)
    os.makedirs(dataset_path)
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
    if bias == 'red': # orange
        red = 1
        green=0.2
        blue = 0
    if bias == 'green':
        green = 1
        blue=0.1
    return np.array([red, green,blue])

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
    color2 = generate_random_color()
    
    A = get_color_matrix(color1, color2)
    return A


if __name__ == '__main__':
    #create_color_task(2)
    X, y, im_path = generate_color_dataset('test',20, 50)

    for i in range(20):
        show_image(X[i, :], y[i])
