'''Виджеты с заданиями к лаб 1.'''

from typing import override
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd  
from tkinter import messagebox as msg
import json
import os
import re

import app
import lab1.funcs as funcs


class Task2(app.TaskFrame):
    '''Лаб 1. Задание 2.
    Открытие фото в окнах разных размеров
    и с разными цвето-фильтрами.'''
    
    def _set_colors_frame(self) -> None:
        _color_spaces = funcs.CV_COLOR_SPACES
        self._color_space_var = tk.IntVar(value=_color_spaces["BGRA"])
        self._colors_frame = ttk.Frame(self._root)
        ttk.Label(
            self._colors_frame,
            text='Цветовые модели:'
        ).pack(expand=True, fill='x')
        
        for k, v in _color_spaces.items():
            ttk.Radiobutton(
                self._colors_frame,
                text=k,
                value=v,
                variable=self._color_space_var
            ).pack(expand=True, fill='x')
            
    def _set_wins_frame(self) -> None:
        _win_flags = funcs.CV_WINDOW_FLAGS
        self._size_var = tk.IntVar(value=_win_flags["NORMAL"])
        self._sizes_frame = ttk.Frame(self._root)
        ttk.Label(
            self._sizes_frame,
            text='Окно:'
        ).pack(expand=True, fill='x')
        
        for k, v in _win_flags.items():
            ttk.Radiobutton(
                self._sizes_frame,
                text=k,
                value=v,
                variable=self._size_var
            ).pack(expand=True, fill='x')
        
    @override
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0,2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0,1), weight=1)
        
        ttk.Label(
            self._root,
            text="Вывод изображения",
        ).grid(row=0, column=0, columnspan=2)
        
        self._set_colors_frame()
        self._colors_frame.grid(row=1, column=0)
        
        self._set_wins_frame()
        self._sizes_frame.grid(row=1, column=1)
        
        ttk.Button(
            self._root,
            text='Выбрать фото...',
            command=self._set_filepath
        ).grid(row=2, column=0)
        
        self._open_btn = ttk.Button(
            self._root,
            text='Открыть',
            state='disabled',
            command=self._set_image
        )
        self._open_btn.grid(row=2, column=1)
        
    def _set_filepath(self) -> None:
        try:
            with open("defaults.json", 'r') as defaults:
                defaults_dict = json.loads(defaults.read())
            default_dir = defaults_dict["images_default_dir"]
        except FileNotFoundError:
            msg.showerror(
                title="Нет файла",
                message="Отсутствует файл defaults.json, проверьте файл и повторите позже."
            )
        else:
            self._filepath = fd.askopenfilename(
                title='Выберите изображение:',
                initialdir=default_dir,
                filetypes=(("*",".png .jpg .jpeg .ico"),)
            )
            if len(self._filepath) != 0:
                if (file_dir:=os.path.dirname(self._filepath)) != default_dir:
                    default_dir = file_dir
                    defaults_dict["images_default_dir"] = default_dir
                    with open("defaults.json", 'w') as defaults:
                        json.dump(defaults_dict, defaults)
                self._open_btn.config(state='normal')
    
    def _set_image(self) -> None:
        size = self._size_var.get()
        color_space = self._color_space_var.get()
        path = self._filepath
        funcs.show_image(
            path,
            win_title=path,
            win_flag=size,
            color_space=color_space
        )
        funcs.close_window(win_title=path)


class Task3(app.TaskFrame):
    '''Лаб 1. Задание 3. Открытие видео с разными фильтрами.'''    
    def _set_colors_frame(self) -> None:
        _color_spaces = funcs.CV_COLOR_SPACES
        self._color_space_var = tk.IntVar(value=_color_spaces['BGRA'])
        self._colors_frame = ttk.Frame(self._root)
        ttk.Label(
            self._colors_frame,
            text='Цветовые модели:'
        ).pack(expand=True, fill='x')
        
        for k, v in _color_spaces.items():
            ttk.Radiobutton(
                self._colors_frame,
                text=k,
                value=v,
                variable=self._color_space_var
            ).pack(expand=True, fill='x')
            
    def _set_wins_frame(self) -> None:
        _win_flags = funcs.CV_WINDOW_FLAGS
        self._win_var = tk.IntVar(value=_win_flags['NORMAL'])
        self._wins_frame = ttk.Frame(self._root)
        ttk.Label(
            self._wins_frame,
            text='Окно:'
        ).pack(expand=True, fill='x')
        
        for k, v in _win_flags.items():
            ttk.Radiobutton(
                self._wins_frame,
                text=k,
                value=v,
                variable=self._win_var
            ).pack(expand=True, fill='x')
    
    @override
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Вывод видео",
        ).grid(row=0, column=0, columnspan=2)
        
        self._set_colors_frame()
        self._colors_frame.grid(row=1, column=0)
        
        self._set_wins_frame()
        self._wins_frame.grid(row=1, column=1)
        
        ttk.Button(
            self._root,
            text='Выбрать видео...',
            command=self._set_filepath
        ).grid(row=2, column=0)
        
        self._play_btn = ttk.Button(
            self._root,
            text='Открыть',
            state='disabled',
            command=self._play_video
        )
        self._play_btn.grid(row=2, column=1)
        
    def _set_filepath(self) -> None:
        try:
            with open("defaults.json", 'r') as defaults:
                defaults_dict = json.loads(defaults.read())
            default_dir = defaults_dict["videos_default_dir"]
        except FileNotFoundError:
            msg.showerror(
                title="Нет файла",
                message="Отсутствует файл defaults.json, проверьте файл и повторите позже."
            )
        else:
            self._filepath = fd.askopenfilename(
                title='Выберите видео:',
                initialdir=default_dir,
                filetypes=(("MP4",".MP4 .mp4"),)
            )
            if len(self._filepath) != 0:
                if (file_dir:=os.path.dirname(self._filepath)) != default_dir:
                    default_dir = file_dir
                    defaults_dict["videos_default_dir"] = default_dir
                    with open("defaults.json", 'w') as defaults:
                        json.dump(defaults_dict, defaults)
                self._play_btn.config(state='normal')
    
    def _play_video(self) -> None:
        path = self._filepath
        size = self._win_var.get()
        color_space = self._color_space_var.get()
        funcs.play_video(
            path,
            win_title=path,
            win_flag=size,
            color_space=color_space
        )


class Task4(app.TaskFrame):
    '''Лаб 1. Задание 4. Записывает видео из файла в другой файл'''
    @override
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Перезапись видео"
        ).grid(row=0, column=0, columnspan=2)
        
        self._choose_btn = ttk.Button(
            self._root,
            text='Выбрать видео...',
            command=self._set_src_path
        )
        self._choose_btn.grid(row=2, column=0)
        
        self._save_btn = ttk.Button(
            self._root,
            text='Сохранить как...',
            state='disabled',
            command=self._save_video
        )
        self._save_btn.grid(row=2, column=1)

    def _set_src_path(self) -> None:
        try:
            with open("defaults.json", 'r') as defaults:
                defaults_dict = json.loads(defaults.read())
            default_dir = defaults_dict["videos_default_dir"]
        except FileNotFoundError:
            msg.showerror(
                title="Нет файла",
                message="Отсутствует файл defaults.json, проверьте файл и повторите позже."
            )
        else:
            self._filepath = fd.askopenfilename(
                title='Выберите видео:',
                initialdir=default_dir,
                filetypes=(("MP4",".MP4 .mp4"),)
            )
            if len(self._filepath) != 0:
                if (file_dir:=os.path.dirname(self._filepath)) != default_dir:
                    default_dir = file_dir
                    defaults_dict["videos_default_dir"] = default_dir
                    with open("defaults.json", 'w') as defaults:
                        json.dump(defaults_dict, defaults)
                self._save_btn.config(state='normal')
        
    def _set_dest_path(self) -> None:
        try:
            with open("defaults.json", 'r') as defaults:
                defaults_dict = json.loads(defaults.read())
            default_dir = defaults_dict["videos_default_dir"]
        except FileNotFoundError:
            msg.showerror(
                title="Нет файла",
                message="Отсутствует файл defaults.json, проверьте файл и повторите позже."
            )
        else:
            self._dest_path = fd.asksaveasfilename(
                title='Сохранить как...',
                initialdir=default_dir,
                initialfile='копия_без_звука.mp4',
                defaultextension='.mp4',
                confirmoverwrite=True
            )
            if len(self._filepath) != 0:
                if (file_dir:=os.path.dirname(self._filepath)) != default_dir:
                    default_dir = file_dir
                    defaults_dict["images_default_dir"] = default_dir
                    with open("defaults.json", 'w') as defaults:
                        json.dump(defaults_dict, defaults)
        
    def _save_video(self) -> None:
        src = self._filepath
        self._set_dest_path()
        dest = self._dest_path
        if len(dest) == 0:
            return
        self._choose_btn.config(state='disabled')
        self._save_btn.config(state='disabled')
        self._root.update()
        funcs.save_video(src, dest)
        self._choose_btn.config(state='normal')
        self._save_btn.config(state='normal')   
    

class Task5(app.TaskFrame):
    '''Лаб 1. Задание 5.
    Прочитать изображение, перевести его в формат HSV.
    Вывести на экран два окна, в одном изображение в формате HSV,
    в другом – исходное изображение.'''
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
                
        ttk.Label(
            self._root,
            text="Два изображения: HSV и BGR"
        ).grid(row=0, column=0, columnspan=2)
        
        self._choose_btn = ttk.Button(
            self._root,
            text='Выбрать файл...',
            command=self._set_src_path
        )
        self._choose_btn.grid(row=2, column=0)
        
        self._show_btn = ttk.Button(
            self._root,
            text='Показать',
            command=self._show_hsv_rgb,
            state="disabled"
        )
        self._show_btn.grid(row=2, column=1)
    
    def _set_src_path(self) -> None:
        try:
            with open("defaults.json", 'r') as defaults:
                defaults_dict = json.loads(defaults.read())
            default_dir = defaults_dict["images_default_dir"]
        except FileNotFoundError:
            msg.showerror(
                title="Нет файла",
                message="Отсутствует файл defaults.json, проверьте файл и повторите позже."
            )
        else:
            self._filepath = fd.askopenfilename(
                title='Выберите изображение:',
                initialdir=default_dir,
                filetypes=(("*",".png .jpg .jpeg .ico"),)
            )
            if len(self._filepath) != 0:
                if (file_dir:=os.path.dirname(self._filepath)) != default_dir:
                    default_dir = file_dir
                    defaults_dict["images_default_dir"] = default_dir
                    with open("defaults.json", 'w') as defaults:
                        json.dump(defaults_dict, defaults)
                self._show_btn.config(state="normal")
                

    def _show_hsv_rgb(self) -> None:
        self._choose_btn.config(state='disabled')
        self._root.update()
        
        path = self._filepath
        
        bgra = funcs.CV_COLOR_SPACES['BGRA']
        hsv = funcs.CV_COLOR_SPACES['HSV']
        funcs.show_image(path, win_title='original', color_space=bgra)
        funcs.move_window(win_title='original', x=300, y=200)
        funcs.show_image(path, win_title='HSV', color_space=hsv)
        funcs.move_window(win_title='HSV', x=900, y=200)
        funcs.close_all()
        
        self._choose_btn.config(state='normal')
        

class Task6(app.TaskFrame):
    '''Лаб 1. Задание 6.
    Прочитать изображение с камеры.
    Вывести в центре на экране Красный крест в формате,
    как на изображении.'''
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Изображение с веб-камеры с красным крестом"
        ).grid(row=0, column=0, columnspan=2)
        
        ttk.Button(
            self._root,
            text='Показать видео',
            command=funcs.show_cam
        ).grid(row=2, column=0, columnspan=2)
            

class Task7(app.TaskFrame):
    '''Лаб 1. Задание 7.
    Отобразить информацию с вебкамеры, записать видео в файл, продемонстрировать видео.'''
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root, 
            text="Запись и отображение видео с веб-камеры"
        ).grid(row=0, column=0, columnspan=2)
        
        self._save_btn = ttk.Button(
            self._root,
            text='Сохранить как...',
            command=self._set_dest_path
        )
        self._save_btn.grid(row=2, column=0)
        
        self._rec_btn = ttk.Button(
            self._root,
            text='Начать запись...',
            state='disabled',
            command=self._record_cam
        )
        self._rec_btn.grid(row=2, column=1)
        
    def _set_dest_path(self) -> None:
        try:
            with open("defaults.json", 'r') as defaults:
                defaults_dict = json.loads(defaults.read())
            default_dir = defaults_dict["videos_default_dir"]
        except FileNotFoundError:
            msg.showerror(
                title="Нет файла",
                message="Отсутствует файл defaults.json, проверьте файл и повторите позже."
            )
        else:
            self._filepath = fd.asksaveasfilename(
                title='Сохранить как...',
                initialdir=default_dir,
                initialfile='запись.mp4',
                defaultextension='.mp4',
                confirmoverwrite=True
            )
            if len(self._filepath) != 0:
                if (file_dir:=os.path.dirname(self._filepath)) != default_dir:
                    default_dir = file_dir
                    defaults_dict["images_default_dir"] = default_dir
                    with open("defaults.json", 'w') as defaults:
                        json.dump(defaults_dict, defaults)
                self._rec_btn.config(state='normal')
    
    def _record_cam(self) -> None:
        dest_path = self._filepath
        funcs.record_cam(dest_path)
        self._rec_btn.config(state='disabled')  
    
                
class Task8(app.TaskFrame):
    '''Лаб 1. Задание 8. Крестовина хамелион'''
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0, 2), weight=1)
        self._root.rowconfigure(index=1, weight=2)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Веб-камера с цветочувствительным центром"
        ).grid(row=0, column=0, columnspan=2)
        
        ttk.Button(
            self._root,
            text='Показать видео',
            command=funcs.show_cam2
        ).grid(row=2, column=0, columnspan=2)
            

class Task9(app.TaskFrame):
    '''Лаб 1. Задание 9. IP-камера'''
    def _set_task(self) -> None:
        self._root.rowconfigure(index=(0,1,2,3), weight=1)
        self._root.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._root,
            text="Трансляция с ip-камеры"
        ).grid(row=0, column=0, columnspan=2)
            
        ttk.Label(
            self._root,
            text="Введите ip-адрес камеры:"
        ).grid(row=1, column=0)
        
        self._ip_var = tk.StringVar(value="")
        self._ip_regex = re.compile(
            "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        )
        self._ip_var.trace_add("write", self._ip_correct)
        
        ttk.Entry(
            self._root,
            textvariable=self._ip_var
        ).grid(row=1, column=1)
        
        self._warning_lbl = ttk.Label(
            self._root,
            text="Неправильно указан ipv4",
            foreground="red"
        )
        self._warning_lbl.grid(row=2, column=0, columnspan=2)
        self._warning_lbl.grid_remove()
        
        self._open_btn = ttk.Button(
            self._root,
            text='Открыть камеру',
            command=self._show_cam,
            state="disabled"
        )
        self._open_btn.grid(row=3, column=0, columnspan=2)
    
    def _ip_correct(self, *_) -> None:
        if self._ip_regex.fullmatch(self._ip_var.get()) is None:
            self._warning_lbl.grid()
            self._open_btn.config(state="disabled")
        else:
            self._warning_lbl.grid_remove()
            self._open_btn.config(state="normal")
            
    def _show_cam(self) -> None:
        ip = self._ip_var.get()
        funcs.play_video(path=ip)

    