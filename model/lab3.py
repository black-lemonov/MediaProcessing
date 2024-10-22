import time

import cv2
import numpy as np

def normalised(matlike):
    return matlike / np.sum(matlike)


def convolution(mat1, mat2) -> float:
    '''Операция свёртки'''
    res = 0
    for i in range(len(mat1)):
        for j in range(len(mat1[i])):
            res += mat1[i][j] * mat2[i][j]
    return res


def gauss(x: int, y: int, sigma: float, mu_x: float, mu_y: float) -> float:
    return 1 / (2 * np.pi * sigma ** 2) * np.e ** (-((x-mu_x)**2 + (y-mu_y)**2)/(2*sigma**2))

    
def gauss_kernel(ksize: int, sigma: float, mu_x: float, mu_y: float):
    kernel = np.empty((ksize, ksize))
    for i in range(ksize):
        for j in range(ksize):
            kernel[i, j] = gauss(i, j, sigma, mu_x, mu_y)
    return kernel

                
def gaussian_blur(img, w: int, h: int, kernel, ksize: int):
    margin = ksize // 2
    blurred = np.zeros((h-margin*2, w-margin*2), np.int16)
    for i in range(margin, h - margin):
        for j in range(margin, w - margin):
            region = img[i-margin: i+margin+1, j-margin: j+margin+1]
            blurred[i-margin, j-margin] = convolution(region, kernel)
    return blurred
            
    
cv2.namedWindow("original")
img = cv2.imread("/home/egorp/Изображения/osaka_smart.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("original", img)
w, h  = img.shape
kernel = gauss_kernel(5, 1.2, 3, 3)
kernel = normalised(kernel)
print(kernel)
blurred = gaussian_blur(img, w, h, kernel, 5) / 255
cv2.namedWindow("blurred")
cv2.imshow("blurred", blurred)
if cv2.waitKey(0) != 27:
    cv2.destroyWindow("blurred")
