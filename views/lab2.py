import tkinter.ttk as ttk

import app
import model.lab2 as lab2

class Task1(app.TaskFrame):
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Камера в HSV"
        ).grid(row=0, column=0, columnspan=2)
        
        ttk.Button(
            self._root,
            text='Включить камеру',
            command=lab2.Task1().main
        ).grid(row=2, column=0, columnspan=2)


class Task2(app.TaskFrame):
    def _set_task(self):
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Фильтрация изображения"
        ).grid(row=0, column=0, columnspan=2)
        
        ttk.Button(
            self._root,
            text='Включить камеру',
            command=lab2.Task2().main
        ).grid(row=2, column=0, columnspan=2)
        

class Task3(app.TaskFrame):
    def _set_task(self):
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Морфологические преобразования"
        ).grid(row=0, column=0, columnspan=2)
        
        ttk.Button(
            self._root,
            text='Включить камеру',
            command=lab2.Task3().main
        ).grid(row=2, column=0, columnspan=2)


class Task4(app.TaskFrame):
    def _set_task(self):
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Моменты изображений"
        ).grid(row=0, column=0, columnspan=2)
        
        ttk.Button(
            self._root,
            text='Включить камеру',
            command=lab2.Task4().main
        ).grid(row=2, column=0, columnspan=2)
        

class Task5(app.TaskFrame):
    def _set_task(self):
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Отслеживание объекта"
        ).grid(row=0, column=0, columnspan=2)
        
        ttk.Button(
            self._root,
            text='Включить камеру',
            command=lab2.Task5().main
        ).grid(row=2, column=0, columnspan=2)
        
    