import tkinter as tk
import tkinter.ttk as ttk 

import main
import lab1


class Builder:
    def __init__(self) -> None:
        self._window = tk.Tk()
        self._labs_nbook = ttk.Notebook(self._window)
        self._labs: list[main.TaskFrame] = []
    
    def set_lab1(self) -> None:
        lab1_frame = ttk.Frame(self._labs_nbook)
        tasks_master = ttk.Notebook(lab1_frame) 
        task2 = lab1.Task2(tasks_master, 'Задание 2')
        task3 = lab1.Task3(tasks_master, 'Задание 3')
        task4 = lab1.Task4(tasks_master, 'Задание 4')
        tasks = (task2, task3, task4)
        self._labs.append(
            main.LabFrame(
                self._labs_nbook,
                lab1_frame,
                tasks_master,
                tasks,
                'Лаб 1'
            )
        )
    
    @property
    def app(self) -> main.App:
        return main.App(
            self._window,
            self._labs_nbook,
            self._labs
        )
    
class Director:
    def min_app(self, builder: Builder) -> main.App:
        builder.set_lab1()
        return builder.app


if __name__ == "__main__":
    director = Director()
    director.min_app(Builder()).run()