from typing import Protocol, Sequence
from abc import abstractmethod

import numpy as np


class ImageOperator(Protocol):
    @property
    @abstractmethod
    def x(self) -> Sequence[Sequence]:
        ...
        
    @property
    @abstractmethod
    def y(self) -> Sequence[Sequence]:
        ...

    @property
    @abstractmethod
    def size(self) -> int:
        ...
        

class SobelOperator(ImageOperator):
    @property
    def x(self) -> np.ndarray:
        return np.array(
            [[-1, 0, 1], 
            [-2, 0, 2], 
            [-1, 0, 1]]
        )
        
    @property
    def y(self) -> np.ndarray:
        return np.array(
            [[-1, -2, -1], 
            [0, 0, 0], 
            [1, 2, 1]]
        )
        
    @property
    def size(self) -> int:
        return 3


class PrewittOperator(ImageOperator):
    @property
    def x(self) -> np.ndarray:
        return np.array(
            [[-1, 0, 1], 
            [-1, 0, 1], 
            [-1, 0, 1]]
        )
        
    @property
    def y(self) -> np.ndarray:
        return np.array(
            [[-1, -1, -1], 
            [0, 0, 0], 
            [1, 1, 1]]
        )
        
    @property
    def size(self) -> int:
        return 3
    
    
class RobertsCrossOperator(ImageOperator):
    @property
    def x(self) -> np.ndarray:
        return np.array(
            [[0, 0, 0], 
            [0, 0, -1], 
            [0, 1, 0]]
        )
        
    @property
    def y(self) -> np.ndarray:
        return np.array(
            [[0, 0, 0], 
            [0, -1, 0], 
            [0, 0, 1]]
        )
        
    @property
    def size(self) -> int:
        return 3