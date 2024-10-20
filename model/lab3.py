import time

import cv2
import numpy as np


def get_gauss_kernel(n: int, sigma: int) -> None:
    '''Ядро для Гауссовского размытия'''
    if n <= 0 or n % 2 == 0:
        raise ValueError("Размерность должна быть положительным нечетным числом!")
    print(f"Size: {n} x {n}. Sigma: {sigma}")
    vect = cv2.getGaussianKernel(n, sigma)
    kernel = vect @ vect.T
    print(kernel)
    

def gauss(x: int, y: int, sigma: int, mu_x: float, mu_y: float) -> float:
    return 1 / (np.pi * sigma ** 2) * np.e ** (((x-mu_x)**2 + (y-mu_y)**2)/(2*sigma**2))


def normalize(mat, dim: int) -> None:
    for i in range(dim):
        for j in range(dim):
            mat[i][j] **= 2
    mat_sum = np.sum(mat)
    for i in range(dim):
        for j in range(dim):
            mat[i][j] /= mat_sum
            mat[i][j] **= 0.5
    
    
def get_gauss_kernel2(ksize: int, sigma: float, mu_x: float, mu_y: float) -> None:
    kernel = np.empty((ksize, ksize))
    for i in range(ksize):
        for j in range(ksize):
            kernel[i,j] = gauss(i, j, sigma, mu_x, mu_y)
    normalize(kernel, ksize)    
    return kernel


def gaussian_blur(img, w: int, h: int, kernel, ksize: int) -> None:
    margin = ksize // 2
    for i in range(margin-1, h - margin):
        for j in range(margin, w - margin):
            val = 0
            for k in range(ksize):
                for l in range(ksize):    
                    val += kernel[k][l] * img[i - margin + k][j - margin + k][0]
            img[i][j] = val
                     

cv2.namedWindow("original")
img = cv2.imread("/home/egorp/Изображения/osaka_smart.jpg")
cv2.imshow("original", img)
w, h, _ = img.shape
kernel = get_gauss_kernel2(5, 1.3, 3, 3)
gaussian_blur(img, w, h, kernel, 5)
cv2.namedWindow("blurred")
cv2.imshow("blurred", img)
if cv2.waitKey(0) != 27:
    cv2.destroyAllWindows()


