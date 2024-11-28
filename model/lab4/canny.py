import numpy as np
import cv2

from edge_detector import EdgeDetector
from image_operators import ImageOperator
from lab3.gaussian_blur import apply_convolution_gray
from utils import get_pixel, get_neighbours


class CannyEdgedetector(EdgeDetector):
    def __init__(self, operator: ImageOperator):
        super().__init__(operator)
        self.__gradient_x: np.ndarray | None = None
        self.__gradient_y: np.ndarray | None = None
        self.__gradient_lengths: np.ndarray | None = None
        self.__gradient_angles: np.ndarray | None = None
        self.__edges: np.ndarray | None = None
    
    def detect(self, img: np.ndarray) -> np.ndarray:
        self.__preprocess_image(img)
        self.__calc_gradients()
        self.__calc_lengths()
        self.__calc_angles()
        self.__supress_nonmax()
        self.__threshold()
        return self.__edges
    
    def __preprocess_image(self, img: np.ndarray) -> None:
        self.__img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        self.__img = cv2.GaussianBlur(self.__img, (3, 3), 2)

    def __calc_gradients(self) -> None:
        self.__gradient_x = apply_convolution_gray(self.__img, self.__operator.x)
        self.__gradient_y = apply_convolution_gray(self.__img, self.__operator.x)
        
    def __calc_lengths(self) -> None:
        self.__gradient_lengths = np.sqrt(
            np.add(
                np.square(self.__gradient_x),
                np.square(self.__gradient_y)
            )
        )
    
    def __calc_angles(self) -> None:
        self.__gradient_angles = np.nan_to_num(np.divide(self.__gradient_y, self.__gradient_x))
        h, w = self.__gradient_angles.shape[0], self.__gradient_angles.shape[1]
        for y in range(h):
            for x in range(w):
                tg = self.__gradient_angles[y, x]
                self.__gradient_angles = get_pixel(x, y, tg)
                
    def __supress_nonmax(self) -> None:
        self.__edges = np.zeros_like(self.__img)
        h, w = self.__edges.shape[0], self.__edges.shape[1] 
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                angle = self.__gradient_angles[y, x]
                n1, n2 = get_neighbours(x, y, angle)
                cur_len = self.__gradient_lengths[y, x]
                if cur_len >= self.__gradient_lengths[*n1] and cur_len > self.__gradient_lengths[*n2]:
                        self.__edges[y, x] = 255
                        
    def __threshold(self) -> None:
        low_percent, high_percent = .25, .75
        
        max_grad_len = self.__gradient_lengths.max()
        
        low_level = int(max_grad_len * low_percent)
        high_level = int(max_grad_len * high_percent)
        
        h, w = self.__edges.shape[0], self.__edges[1]
        for y in range(h):
            for x in range(w):
                if self.__edges[y, x] <= 0:
                    continue
                
                cur_len = self.__gradient_lengths[y, x]
                
                if cur_len < low_level:
                    self.__edges[y, x] = 0
                    continue
                
                if cur_len >= high_level:
                    continue
                
                keep = False
                
                for y0 in (y - 1, y, y + 1):
                    for x0 in (x - 1, x, x + 1):
                        if y0 == y and x0 == x:
                            continue
                        if self.__edges[y0, x0] <= 0 or self.__gradient_lengths[y0, x0] < high_level: 
                            self.__edges[y, x] = 0
                            break
                    
    