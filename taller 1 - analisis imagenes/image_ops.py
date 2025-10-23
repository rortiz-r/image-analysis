import numpy as np

class ImageOps():
    def __init__(self):

        pass
    
    def truncate(self, image):

        value_r = image

        if image > 255.0:
            value_r = 255.0
        elif image < 0.0:
            value_r = 0.0

        return value_r


    def add_images(self, A,B, alpha):
		
        A, B = np.array(A,dtype=np.int16), np.array(B,dtype=np.float32)

        M,N,O = A.shape

        result = np.zeros((M,N,O))

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = self.truncate(alpha * A[i,j,k] +(1-alpha)*B[i,j,k])

        return result.astype(np.uint8)
	

    def subtract_images(self, A,B):
       
        A, B = np.array(A,dtype=np.int16), np.array(B,dtype=np.float32)
		
        M,N,O = A.shape

        result = np.zeros((M,N,O))

        result = A - B

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = self.truncate(A[i,j,k] - B[i,j,k])


        return result.astype(np.uint8)


    def multiply_images(self, A,B):

        A, B = np.array(A,dtype=np.float32), np.array(B,dtype=np.float32)
		
        M,N,O = A.shape

        result = np.zeros((M,N,O))

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = self.truncate(A[i,j,k] * B[i,j,k])

        return result.astype(np.uint8)

    

    def square_scalar(self, A):
        image = np.array(A, dtype=np.float32)
        
        M,N,O = image.shape

        result = np.zeros((M,N,O))

        # Normalization and power of two
        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = self.truncate((image[i,j,k])**2)



        return result.astype(np.uint8)


    def cubic_scalar(self, A):

        image = np.array(A, dtype=np.float32)

        M,N,O = image.shape
        
        result = np.zeros((M,N,O))

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = self.truncate((image[i,j,k])**3)

        return result.astype(np.uint8)
        
    def add_scalar(self, A, scalar):

        print(scalar)

        image = np.array(A, dtype=np.float32)
        M,N,O = image.shape

        result = np.zeros((M,N,O))

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    result[i,j,k] = self.truncate((image[i,j,k]) + scalar)

        return result.astype(np.uint8)


    def subtract_scalar(self, A, scalar):


        image = np.array(A,dtype=np.float32)
		
        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = self.truncate((image[i,j,k]) - scalar)

        return image.astype(np.uint8)


    def multiply_scalar(self, A, scalar):

        image = np.array(A,dtype=np.float32)
		
        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = self.truncate((image[i,j,k]) * scalar)

        return image.astype(np.uint8)


    def divide_scalar(self, A, scalar):
		
        image = np.array(A,dtype=np.float32)
		
        M,N,O = image.shape

        for i in range(M):
            for j in range(N):
                for k in range(O):
                    image[i,j,k] = self.truncate((image[i,j,k]) / scalar)

        return image.astype(np.uint8)


    
