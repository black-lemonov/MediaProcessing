from typing import Final
import math as m

import numpy as np
import cv2

from edge_detector import EdgeDetector
from image_operators import ImageOperator, SobelOperator, PrewittOperator, RobertsCrossOperator
import model.lab3.gaussian_blur as lab3

class CannyEdgeDetector(EdgeDetector):
    BLUR_KSIZE: tuple[int, int] = (5, 5)
    LOW_THRESHOLD_PERCENTAGE: int = 2 
    TOP_THRESHOLD_PERCENTAGE: int = 7
    
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
        self._img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self._img = cv2.GaussianBlur(self._img, self.BLUR_KSIZE, 0)

    def __calc_gradients(self) -> None:
        self.__gradient_x = lab3.apply_convolution_gray(self._img, self._operator.x, self._operator.size)
        self.__gradient_y = lab3.apply_convolution_gray(self._img, self._operator.y, self._operator.size)
        
    def __calc_lengths(self) -> None:
        h, w = self.__gradient_x.shape[0], self.__gradient_x.shape[1]
        self.__gradient_lengths = np.zeros((h, w))
        for y in range(h):
            for x in range(w):
                x_val = self.__gradient_x[y, x]
                y_val = self.__gradient_y[y, x]
                self.__gradient_lengths[y, x] = m.sqrt(m.pow(x_val, 2) + m.pow(y_val, 2))
    
    def __calc_angles(self) -> None:
        h, w = self.__gradient_x.shape[0], self.__gradient_x.shape[1]
        self.__gradient_angles = np.zeros((h, w), np.ushort)
        for y in range(h):
            for x in range(w):
                x_val = self.__gradient_x[y, x]
                y_val = self.__gradient_y[y, x]
                tg = self.calc_tangens(y_val, x_val)
                self.__gradient_angles[y, x] = self.get_pixel(x, y, tg)
                
    def __supress_nonmax(self) -> None:
        self.__edges = np.zeros_like(self._img)
        h, w = self.__edges.shape[0], self.__edges.shape[1] 
        for y in range(2, h - 2):
            for x in range(2, w - 2):
                angle = self.__gradient_angles[y-1, x-1]
                n1, n2 = self.get_neighbours(x-1, y-1, angle)
                cur_len = self.__gradient_lengths[y-1, x-1]
                if cur_len >= self.__gradient_lengths[*n1] and cur_len > self.__gradient_lengths[*n2]:
                    self.__edges[y, x] = 255
                        
    def __threshold(self) -> None:
        max_grad_len = self.__gradient_lengths.max()
        
        low_value = int(max_grad_len * self.LOW_THRESHOLD_PERCENTAGE / 100)
        high_value = int(max_grad_len * self.TOP_THRESHOLD_PERCENTAGE / 100)
        
        h, w = self.__edges.shape[0], self.__edges.shape[1]
        for y in range(h):
            for x in range(w):
                if self.__edges[y, x] <= 0:
                    continue
                
                cur_len = self.__gradient_lengths[y, x]
                
                if cur_len < low_value:
                    self.__edges[y, x] = 0
                    continue
                
                if cur_len >= high_value:
                    continue
                
                self.__check_neighbours(x, y, high_value)
    
    def __check_neighbours(self, x: int, y: int, threshold_value: int) -> None:
        for y0 in (y - 1, y, y + 1):
            for x0 in (x - 1, x, x + 1):
                if y0 == y and x0 == x:
                    continue
                if self.__edges[y0, x0] <= 0 or self.__gradient_lengths[y0, x0] < threshold_value: 
                    self.__edges[y, x] = 0
                    return
    
    @property
    def angles(self) -> np.ndarray:
        return (self.__gradient_angles * 255 / 7).astype(np.uint8)
    
    
    @property
    def lengths(self) -> np.ndarray:
        return (self.__gradient_lengths / self.__gradient_lengths.max() * 255).astype(np.uint8)
    
    
    @staticmethod
    def get_pixel(x, y, tg):
        if all((x >= 0, y <= 0, tg < -2.414)) or all((x <= 0, y <= 0, tg > 2.414)):
            return 0
        elif all((x >= 0, y <= 0, tg < -0.414)):
            return 1
        elif all((x >= 0, y <= 0, tg > -0.414)) or all((x >= 0, y >= 0, tg < 0.414)):
            return 2
        elif all((x >= 0, y >= 0, tg < 2.414)):
            return 3
        elif all((x >= 0, y >= 0, tg > 2.414)) or all((x <= 0, y >= 0, tg < -2.414)):
            return 4
        elif all((x <= 0, y >= 0, tg < -0.414)):
            return 5
        elif all((x <= 0, y >= 0, tg > -0.414)) or all((x <= 0, y <= 0, tg < 0.414)):
            return 6
        elif all((x <= 0, y <= 0, tg < 2.414)):
            return 7
        

    @staticmethod
    def get_neighbours(x, y, angle: int) -> tuple[tuple[int, int], tuple[int, int]]:
        if angle == 0 or angle == 4:
            neighbour1 = (y - 1, x)
            neighbour2 = (y + 1, x)
        elif angle == 1 or angle == 5:
            neighbour1 = (y - 1, x + 1)
            neighbour2 = (y + 1, x - 1)
        elif angle == 2 or angle == 6:
            neighbour1 = (y, x + 1)
            neighbour2 = (y, x - 1)
        elif angle == 3 or angle == 7:
            neighbour1 = (y + 1, x + 1)
            neighbour2 = (y - 1, x - 1)
        
        return neighbour1, neighbour2


    @staticmethod
    def calc_tangens(y: int, x: int) -> float:
        return y / x if x != 0 else np.inf if y >= 0 else -np.inf  
                
    
class CannyDirector:
    def roberts(self) -> CannyEdgeDetector:
        return CannyEdgeDetector(RobertsCrossOperator())
    
    def sobel(self) -> CannyEdgeDetector:
        return CannyEdgeDetector(SobelOperator())
    
    def prewitt(self) -> CannyEdgeDetector:
        return CannyEdgeDetector(PrewittOperator())
    
    
director: Final[CannyDirector] = CannyDirector()