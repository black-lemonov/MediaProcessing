import tkinter as tk
import tkinter.ttk as ttk 
from abc import ABC, abstractmethod
from typing import Literal, Optional

from ttkthemes import ThemedTk
from overrides import override

import main
import lab1


class Builder(ABC):
    @abstractmethod
    def set_lab1(self) -> None:
        pass
    
    @abstractmethod
    def set_lab2(self) -> None:
        pass
    
    @abstractmethod
    def set_lab3(self) -> None:
        pass
    
    @property
    @abstractmethod
    def app(self) -> main.App:
        pass


class TkBuilder(Builder):
    def __init__(self) -> None:
        self._set_window()
        self._labs_nbook = ttk.Notebook(self._window)
        self._labs: list[main.LabFrame] = []
        
    def _set_window(self) -> None:
        self._window = tk.Tk()
    
    def set_lab1(self) -> None:
        lab1_frame = ttk.Frame(self._labs_nbook)
        tasks_master = ttk.Notebook(lab1_frame) 
        task2 = lab1.Task2(tasks_master, 'Задание 2')
        task3 = lab1.Task3(tasks_master, 'Задание 3')
        task4 = lab1.Task4(tasks_master, 'Задание 4')
        task5 = lab1.Task5(tasks_master, 'Задание 5')
        task6 = lab1.Task6(tasks_master, 'Задание 6')
        task7 = lab1.Task7(tasks_master, 'Задание 7')
        task8 = lab1.Task8(tasks_master, 'Задание 8')
        task9 = lab1.Task9(tasks_master, 'Задание 9')
        tasks = (task2, task3, task4, task5, task6, task7, task8, task9)
        self._labs.append(
            main.LabFrame(
                self._labs_nbook,
                lab1_frame,
                tasks_master,
                tasks,
                'Лаб 1'
            )
        )
        
    def set_lab2(self) -> None:
        raise NotImplementedError
    
    def set_lab3(self) -> None:
        raise NotImplementedError
    
    @property
    def app(self) -> main.App:
        return main.App(
            self._window,
            self._labs_nbook,
            self._labs
        )
        

class ThemedTkBuilder(TkBuilder):
    def __init__(self,
                 theme: Optional[Literal['arc', 'blue', 'clearlooks', 'elegane', 'kroc', 'plastik', 'radiance', 'ubuntu', 'winxpblue']] = None) -> None:
        self._theme = theme
        super().__init__()

    @override
    def _set_window(self) -> None:
        self._window = ThemedTk(theme=self._theme)
    
    
class Director:
    def min_app(self, builder: Builder) -> main.App:
        builder.set_lab1()
        return builder.app


if __name__ == "__main__":
    director = Director()
    director.min_app(ThemedTkBuilder(theme='plastik')).run()