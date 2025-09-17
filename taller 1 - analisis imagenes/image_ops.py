import numpy as np

class ImageOps():
    def __init__(self):

        pass
    
    def add_images(self, A,B, alpha):
		
        A, B = np.array(A,dtype=np.float32), np.array(B,dtype=np.float32)

        M,N,O = A.shape

        result = np.zeros((M,N,O))

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = alpha * A[i,j,k] +(1-alpha)*B[i,j,k]
            

        return (np.clip(result, 0, 255).astype(np.uint8))
	

    def subtract_images(self, A,B):
       
        A, B = np.array(A,dtype=np.float32), np.array(B,dtype=np.float32)
		
        M,N,O = A.shape

        result = np.zeros((M,N,O))

        result = A - B

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = A[i,j,k] - B[i,j,k]


        return np.clip(result, 0, 255).astype(np.uint8)


    def multiply_images(self, A,B):

        A, B = np.array(A,dtype=np.float32), np.array(B,dtype=np.float32)
		
        M,N,O = A.shape

        result = np.zeros((M,N,O))

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = A[i,j,k] * B[i,j,k]

        return (np.clip(result, 0, 255).astype(np.uint8))

    

    def square_scalar(self, A):
        image = np.array(A, dtype=np.float32)
        
        M,N,O = image.shape

        # Normalization and power of two
        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = (image[i,j,k]/255.0)**2



        return image


    def cubic_scalar(self, A):

        image = np.array(A, dtype=np.float32)

        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = (image[i,j,k]/255.0)**3

        return image
        
    def add_scalar(self, A, scalar):

        image = np.array(A, dtype=np.float32)
        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = (image[i,j,k]/255.0) + scalar

        return (np.clip(image, 0, 1))


    def subtract_scalar(self, A, scalar):


        image = np.array(A,dtype=np.float32)
		
        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = (image[i,j,k]/255.0) - scalar

        return (np.clip(image, 0, 1))


    def multiply_scalar(self, A, scalar):

        image = np.array(A,dtype=np.float32)
		
        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = (image[i,j,k]/255.0) * scalar

        return (np.clip(image, 0, 1))


    def divide_scalar(self, A, scalar):
		
        image = np.array(A,dtype=np.float32)
		
        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = (image[i,j,k]/255.0) / scalar

        return (np.clip(image, 0, 1))


    
