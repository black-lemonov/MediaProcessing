from __future__ import annotations
from typing import Iterable
from tkinter import Tk, ttk
from abc import ABC, abstractmethod
from sys import exit

from ttkthemes import ThemedTk


class App:
    '''Приложение с лабами'''
    def __init__(self,
                 window: Tk | ThemedTk,
                 labs_master: ttk.Notebook = None,
                 labs: Iterable[LabFrame] = None) -> None:
        self._window = window
        self._labs_master = labs_master
        self._labs = labs
        self._set_window()
        self._set_labs()
    
    def _set_window(self) -> None:
        '''Создание окна'''
        self._window.title("Алгоритмы цифровой обработки мультимедиа")
        self._window.geometry('760x540+400+200')
        self._window.wm_protocol('WM_DELETE_WINDOW', exit)
        
    def _set_labs(self) -> None:
        '''Добавление окон с лабами'''
        if self._labs_master is None or self._labs is None:
            return
        self._labs_master.pack(expand=True, fill='both')
        for lab in self._labs:
            self._labs_master.add(lab.frame, text=lab.title)
            
    def run(self) -> None:
        self._window.mainloop()


class LabFrame:
    '''Frame с лабой'''
    def __init__(self,
                 nbook: ttk.Notebook,
                 root: ttk.Frame,
                 tasks_master: ttk.Notebook,
                 tasks: tuple[TaskFrame],
                 title: str) -> None:
        self._nbook = nbook
        self._root = root
        self._tasks_master = tasks_master
        self._tasks = tasks
        self._title = title
        self._set_tasks()
    
    def _set_tasks(self) -> None:
        '''Добавление окон с заданиями'''
        self._tasks_master.pack(expand=True, fill='both')
        for task in self._tasks:
            self._tasks_master.add(task.frame, text=task.title)
        
    @property
    def frame(self) -> ttk.Frame:
        '''Frame на котором все расположено'''
        return self._root
    
    @property
    def title(self) -> str:
        return self._title
    
    
class TaskFrame(ABC):
    '''Frame с заданием из лабы'''
    def __init__(self, nbook: ttk.Notebook, title: str) -> None:
        self._nbook = nbook
        self._title = title
        self._set_root()
        self._set_task()
    
    def _set_root(self) -> None:
        '''Создание Frame на котором все расположено'''
        self._root = ttk.Frame(self._nbook)
        self._root.pack(expand=True, fill="both")
            
    @abstractmethod
    def _set_task(self) -> None:
        '''Создание виджетов, связанных с заданием'''
        pass
        
    @property
    def frame(self) -> ttk.Frame:
        '''Frame на котором все расположено'''
        return self._root
    
    @property
    def title(self) -> str:
        return self._title
    