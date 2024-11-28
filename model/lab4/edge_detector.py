from typing import Iterable
from abc import ABC, abstractmethod

from image_operators import ImageOperator


class EdgeDetector(ABC):
    def __init__(self, operator: ImageOperator):
        self.__operator: ImageOperator = operator
        self.__img: Iterable[Iterable] | None = None
        
    @abstractmethod
    def detect(self, img: Iterable[Iterable]) -> Iterable[Iterable]:
        """Возвращает изображение с обнаруженными границами"""
        ...
        