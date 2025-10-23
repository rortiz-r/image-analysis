import numpy as np

class GeometricOps():
    def __init__(self):

        pass


    
    def rotation(self, theta, image):

        image = np.array(image, dtype=np.float32)/255.0
        theta = np.radians(theta)

        M,N,O = image.shape

        cx = (M//2)
        cy = (N//2) 

        result = np.zeros((M, N, O))

        for x in range(M):
            for y in range(N):
                ## Aplicamos rotación inversa
                
                x_c = x - cx
                y_c = y-cy

                new_x = int((np.cos(-theta)*x_c) - (np.sin(-theta)*y_c)) +cx 
                new_y = int((np.sin(-theta)*x_c) + (np.cos(-theta)*y_c)) +cy

                if new_x < M and new_y < N:
                    result[new_x, new_y] = image[x,y]/image.max()



        return result




    def traslation(self, bx, by, image):

        image = np.array(image, dtype=np.float32)/255.0
        M,N,O = image.shape

        result = np.zeros((M, N, O))

        ### crear matriz de coordenadas
        for x in range(M):
            for y in range(N):
                for z in range(O):
                    new_x = x + bx
                    new_y = y + by
                    if(new_x < M and new_y < N):
                        result[new_x, new_y, z] = image[x,y,z] 
        return result
	