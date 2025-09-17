import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def traslation(bx, by):

    image = Image.open("../image_test/bird2.png").resize((300,300))

    image = np.array(image, dtype=np.float32)/ 255.0 # Normalizamos imagen }

    M,N,O = image.shape
    
    result = np.zeros((M, N, O))

    coord = np.zeros((M, N, O))

    coord = np.zeros((M, N, O))
    ### crear matriz de coordenadas
    for x in range(M):
        for y in range(N):
            for z in range(O):
                print(f"{x}{y}")
                new_x = x + bx
                new_y = y + by
                if(new_x < M and new_y < N):
                    result[new_x, new_y, z] = image[x,y,z]
                                



    plt.imshow(result)
    plt.show()

    pass



def rotation(theta):

    theta = np.radians(theta)

    image = Image.open("../image_test/bird2.png").resize((500,500))

    image = np.array(image, dtype=np.float32)/ 255.0 # Normalizamos imagen }

    M,N,O = image.shape
    

    #Matriz de rotacion
    rotation_matrix = np.array(([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]))
    ## Crear matriz de coordenadas


    x_coords, y_coords = np.meshgrid(np.arange(M), np.arange(N))

    coords = np.vstack([x_coords.flatten(), y_coords.flatten()])
    

    rotated_coord = rotation_matrix @ coords
    rotated_coord = rotated_coord.astype(int)
    rotated_coord[0] += -min(rotated_coord[0])
    rotated_coord[1] += -min(rotated_coord[1])
    
    result = np.zeros((rotated_coord[0].max() + 1, rotated_coord[1].max() + 1,O))
    
    result[rotated_coord[0], rotated_coord[1], :] = image.reshape(-1,O)





    plt.imshow(result)
    plt.show()
    pass
                



traslation(80, 80)