import tkinter as tk
import tkinter.ttk as ttk 
from abc import ABC, abstractmethod
from typing import Literal, override

from ttkthemes import ThemedTk

import app as app
import views.lab1 as lab1
import views.lab2 as lab2


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
    def app(self) -> app.App:
        pass


class TkBuilder(Builder):
    def __init__(self) -> None:
        self._set_window()
        self._labs_nbook = ttk.Notebook(self._window)
        self._labs: list[app.LabFrame] = []
        
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
            app.LabFrame(
                self._labs_nbook,
                lab1_frame,
                tasks_master,
                tasks,
                'Лаб 1'
            )
        )
        
    def set_lab2(self) -> None:
        lab2_frame = ttk.Frame(self._labs_nbook)
        tasks_master = ttk.Notebook(lab2_frame) 
        task1 = lab2.Task1(tasks_master, 'Задание 1')
        task2 = lab2.Task2(tasks_master, 'Задание 2')
        task3 = lab2.Task3(tasks_master, 'Задание 3')
        task4 = lab2.Task4(tasks_master, 'Задание 4')
        task5 = lab2.Task5(tasks_master, 'Задание 5')
        tasks = (task1, task2, task3, task4, task5)
        self._labs.append(
            app.LabFrame(
                self._labs_nbook,
                lab2_frame,
                tasks_master,
                tasks,
                'Лаб 2'
            )
        )
    
    def set_lab3(self) -> None:
        raise NotImplementedError
    
    @property
    def app(self) -> app.App:
        return app.App(
            self._window,
            self._labs_nbook,
            self._labs
        )
        

class ThemedTkBuilder(TkBuilder):
    def __init__(self,
                 theme: Literal['arc', 'blue', 'clearlooks', 'elegance', 'kroc', 'plastik', 'radiance', 'ubuntu', 'winxpblue'] | None = None) -> None:
        self._theme = theme
        super().__init__()

    @override
    def _set_window(self) -> None:
        self._window = ThemedTk(theme=self._theme)
    
    
class Director:
    def min_app(self, builder: Builder) -> app.App:
        builder.set_lab1()
        builder.set_lab2()
        return builder.app
        