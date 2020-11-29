import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
def generate_image_samples(num_squares:int, num_circles:int):
    # Create figure and axes
    im = np.full((200,200,3),255)
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)
    for i in range(num_squares):# Add Rectangles
        
        x = random.choice(range(170))
        y = random.choice(range(170))
        rect = patches.Rectangle((x,y),40,30,linewidth=1,edgecolor='g',facecolor='none')
        ax.add_patch(rect)
        print(x,y)
    for i in range(num_circles): # Add Circles
        # Create a Rectangle patch
        x = random.choice(range(20,180))
        y = random.choice(range(20,180))
        rect = patches.Circle((x,y),20, linewidth=1,edgecolor='b',facecolor='none')
        ax.add_patch(rect)
    
    plt.show()

generate_image_samples(5,3)