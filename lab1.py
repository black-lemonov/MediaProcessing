from typing import Iterable, override
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd  
from tkinter import messagebox as msg
import time
import json
import os

import cv2

import main


class Task2(main.TaskFrame):
    '''Лаб 1. Задание 2.
    Открытие фото в окнах разных размеров
    и с разными цвето-фильтрами.'''
    
    def _set_colors_frame(self) -> None:
        _color_spaces: dict[str, int] = {
            'BGRA': cv2.COLOR_BGR2BGRA,
            'GRAY': cv2.COLOR_BGR2GRAY,
            'LUV': cv2.COLOR_BGR2LUV,
            'HLS': cv2.COLOR_BGR2HLS,
            'HSV': cv2.COLOR_BGR2HSV,
            'YCrCb': cv2.COLOR_BGR2YCrCb,
            'YUV': cv2.COLOR_BGR2YUV,
        }
        self._color_space_var = tk.IntVar(value=_color_spaces['BGRA'])
        self._colors_frame = ttk.Frame(self._main_frame)

        ttk.Label(self._colors_frame, text='Цветовые модели:').pack(expand=True, fill='x')
        
        for k, v in _color_spaces.items():
            ttk.Radiobutton(
                self._colors_frame,
                text=k,
                value=v,
                variable=self._color_space_var
            ).pack(expand=True, fill='x')
            
    def _set_wins_frame(self) -> None:
        _win_flags: dict[str, int] = {
            'NORMAL': cv2.WINDOW_GUI_NORMAL,
            'FULLSCREEN': cv2.WINDOW_FULLSCREEN,
            'KEEPRATIO': cv2.WND_PROP_ASPECT_RATIO
        }
        self._size_var = tk.IntVar(value=_win_flags['NORMAL'])
        self._sizes_frame = ttk.Frame(self._main_frame)

        ttk.Label(self._sizes_frame, text='Окно:').pack(expand=True, fill='x')
        
        for k, v in _win_flags.items():
            ttk.Radiobutton(
                self._sizes_frame,
                text=k,
                value=v,
                variable=self._size_var
            ).pack(expand=True, fill='x')
        
    @override
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        self._main_frame.rowconfigure(index=(0,2), weight=1)
        self._main_frame.rowconfigure(index=1, weight=2)
        self._main_frame.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._main_frame,
            text="Вывод изображения",
        ).grid(row=0, column=0, columnspan=2)
        
        self._set_colors_frame()
        self._colors_frame.grid(row=1, column=0)
        
        self._set_wins_frame()
        self._sizes_frame.grid(row=1, column=1)
        
        ttk.Button(
            self._main_frame,
            text='Выбрать фото...',
            command=self._set_filepath
        ).grid(row=2, column=0)
        
        self._open_btn = ttk.Button(
            self._main_frame,
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
        photo = self._filepath
        self.show_image(photo, photo, size, color_space)
        if cv2.waitKey(0) == 27:
            cv2.destroyWindow(photo)
    
    @staticmethod
    def show_image(path: str,
                   win_title: str = 'image',
                   win_flag: int = cv2.WINDOW_NORMAL,
                   color_space: int = cv2.COLOR_BGR2RGBA) -> None:        
        frame = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        cv2.namedWindow(win_title, win_flag) 
        colored_frame = cv2.cvtColor(frame, color_space)
        cv2.imshow(win_title, colored_frame)


class Task3(main.TaskFrame):
    '''Лаб 1. Задание 3. Открытие видео с разными фильтрами.'''    
    def _set_colors_frame(self) -> None:
        _color_spaces: dict[str, int] = {
            'BGRA': cv2.COLOR_BGR2BGRA,
            'GRAY': cv2.COLOR_BGR2GRAY,
            'LUV': cv2.COLOR_BGR2LUV,
            'HLS': cv2.COLOR_BGR2HLS,
            'HSV': cv2.COLOR_BGR2HSV,
            'YCrCb': cv2.COLOR_BGR2YCrCb,
            'YUV': cv2.COLOR_BGR2YUV,
        }
        self._color_space_var = tk.IntVar(value=_color_spaces['BGRA'])
        self._colors_frame = ttk.Frame(self._main_frame)

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
        _win_flags: dict[str, int] = {
            'NORMAL': cv2.WINDOW_GUI_NORMAL,
            'FULLSCREEN': cv2.WINDOW_FULLSCREEN,
            'KEEPRATIO': cv2.WND_PROP_ASPECT_RATIO
        }
        self._win_var = tk.IntVar(value=_win_flags['NORMAL'])
        self._wins_frame = ttk.Frame(self._main_frame)

        ttk.Label(self._wins_frame, text='Окно:').pack(expand=True, fill='x')
        
        for k, v in _win_flags.items():
            ttk.Radiobutton(
                self._wins_frame,
                text=k,
                value=v,
                variable=self._win_var
            ).pack(expand=True, fill='x')
    
    @override
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        self._main_frame.rowconfigure(index=1, weight=2)
        self._main_frame.rowconfigure(index=(0, 2), weight=1)
        self._main_frame.columnconfigure(index=(0, 1), weight=1)
        
        ttk.Label(
            self._main_frame,
            text="Вывод видео",
        ).grid(row=0, column=0, columnspan=2)
        
        self._set_colors_frame()
        self._colors_frame.grid(row=1, column=0)
        
        self._set_wins_frame()
        self._wins_frame.grid(row=1, column=1)
        
        ttk.Button(
            self._main_frame,
            text='Выбрать видео...',
            command=self._set_filepath
        ).grid(row=2, column=0)
        
        self._play_btn = ttk.Button(
            self._main_frame,
            text='Открыть',
            state='disabled',
            command=self._set_video
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
    
    def _set_video(self) -> None:
        video = self._filepath
        size = self._win_var.get()
        color_space = self._color_space_var.get()
        self.play_video(video, video, size, color_space)
    
    @staticmethod
    def play_video(path: str,
                   win_title: str = 'video',
                   win_flag: int = cv2.WINDOW_NORMAL,
                   color_space: int = cv2.COLOR_BGR2RGBA) -> None:
        cap = cv2.VideoCapture(path)
        
        if not cap.isOpened():
            return
        
        cv2.namedWindow(win_title, win_flag)        
        while cap.grab():
            frame = cap.read()[1]
            colored_frame = cv2.cvtColor(frame, color_space)
            cv2.imshow(win_title, colored_frame)
            if cv2.waitKey(60) == 27:
                cap.release()
                cv2.destroyWindow(win_title)
                break


class Task4(main.TaskFrame):
    '''Лаб 1. Задание 4. Записывает видео из файла в другой файл'''
    @override
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        ttk.Label(
            self._main_frame,
            text="Запись видео"
        ).pack(expand=True)
        
        self._choose_btn = ttk.Button(
            self._main_frame,
            text='Выбрать видео...',
            command=self._set_src_path
        )
        self._choose_btn.pack(expand=True)
        
        self._save_btn = ttk.Button(
            self._main_frame,
            text='Сохранить как...',
            state='disabled',
            command=self._save_video
        )
        self._save_btn.pack(expand=True)

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
        
    def _save_video(self) -> None:
        src = self._filepath
        self._set_dest_path()
        dest = self._dest_path
        if len(dest) == 0:
            return
        self._choose_btn.config(state='disabled')
        self._save_btn.config(state='disabled')
        self._main_frame.update()
        self.save_video(src, dest)
        self._choose_btn.config(state='normal')
        self._save_btn.config(state='normal')   
    
    @staticmethod 
    def save_video(src_path: str, dest_path: str) -> None:        
        vid_reader = cv2.VideoCapture(src_path)
        
        if not vid_reader.isOpened():
            msg.showerror(title="Ошибка", message="Видео не было открыто. Проверьте путь к источнику.")
            return
        
        w = int(vid_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(vid_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps= float(vid_reader.get(cv2.CAP_PROP_FPS))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        vid_writer = cv2.VideoWriter(dest_path, fourcc, fps, frameSize=(w, h))
        
        if not vid_writer.isOpened():
            msg.showerror(title="Ошибка", message="Файл назначения не был создан. Проверьте путь назначения.")
            return
        
        while vid_reader.grab():
            frame = vid_reader.read()[1]
            vid_writer.write(frame)
        
        vid_reader.release()
        vid_writer.release()
        msg.showinfo(title="Успех", message=f'Видео успешно сохранено в: {dest_path} .')  
    

class Task5(main.TaskFrame):
    '''Лаб 1. Задание 5.
    Прочитать изображение, перевести его в формат HSV.
    Вывести на экран два окна, в одном изображение в формате HSV,
    в другом – исходное изображение.'''
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        ttk.Label(
            self._main_frame,
            text="Два изображения: HSV и BGR"
        ).pack(expand=True)
        
        self._choose_btn = ttk.Button(
            self._main_frame,
            text='Выбрать файл...',
            command=self._set_src_path
        )
        self._choose_btn.pack(expand=True)
        
        self._show_btn = ttk.Button(
            self._main_frame,
            text='Показать',
            command=self._show_hsv_rgb,
            state="disabled"
        )
        self._show_btn.pack(expand=True)
    
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
        
        image_path = self._filepath
        
        Task2.show_image(image_path, 'original')
        cv2.moveWindow('original', 300, 200)
        Task2.show_image(image_path, 'HSV', color_space=cv2.COLOR_BGR2HSV)
        cv2.moveWindow('HSV', 900, 200)
        
        if cv2.waitKey(0) == 27:
            cv2.destroyAllWindows()
        
        self._choose_btn.config(state='normal')
        

class Task6(main.TaskFrame):
    '''Лаб 1. Задание 6.
    Прочитать изображение с камеры.
    Вывести в центре на экране Красный крест в формате,
    как на изображении.'''
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        ttk.Label(
            self._main_frame,
            text="Изображение с веб-камеры с красным крестом"
        ).pack(expand=True)
        
        ttk.Button(
            self._main_frame,
            text='Показать видео',
            command=self._show_cam
        ).pack(expand=True)
    
    def _show_cam(self) -> None:
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("cam", cv2.WINDOW_AUTOSIZE)
        
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        width = 40

        top_left_1: tuple[int, int] = (w//2 - width//2, width//2)
        bottom_right_1: tuple[int, int] = (w//2 + width//2, h - width//2)

        top_left_2: tuple[int, int] = (width//2, h//2 - width//2)
        bottom_right_2: tuple[int, int] = (w - width//2, h//2 + width//2)

        red_color: tuple[int, int, int] = (0, 0, 255)

        while cap.grab():
            frame = cap.read()[1]

            frame = cv2.rectangle(frame, top_left_1, bottom_right_1, red_color, 2)
            frame = cv2.rectangle(frame, top_left_2, bottom_right_2, red_color, 2)
            cv2.imshow("cam", frame)
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyWindow("cam")
                break
            

class Task7(main.TaskFrame):
    '''Лаб 1. Задание 7.
    Отобразить информацию с вебкамеры, записать видео в файл, продемонстрировать видео.'''
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        ttk.Label(
            self._main_frame, 
            text="Запись и отображение видео с веб-камеры"
        ).pack(expand=True)
        
        self._save_btn = ttk.Button(
            self._main_frame,
            text='Сохранить как...',
            command=self._set_dest_path
        )
        self._save_btn.pack(expand=True)
        
        self._rec_btn = ttk.Button(
            self._main_frame,
            text='Начать запись...',
            state='disabled',
            command=self._record_cam
        )
        self._rec_btn.pack(expand=True)
        
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
                initialfile='запись.mp4',
                defaultextension='.mp4',
                confirmoverwrite=True
            )
            if len(self._dest_path) != 0:
                self._rec_btn.config(state='normal')
    
    def _record_cam(self) -> None:
        dest_path = self._dest_path
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("cam", cv2.WINDOW_AUTOSIZE)
        
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps= float(cap.get(cv2.CAP_PROP_FPS))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        vid_writer = cv2.VideoWriter(dest_path, fourcc, fps, frameSize=(w, h))
        
        if not vid_writer.isOpened():
            msg.showerror(title="Ошибка", message="Файл назначения не был создан. Проверьте путь назначения.")
            return

        while cap.grab():
            frame = cap.read()[1]
            cv2.putText(
                frame,
                f'win size: {w}x{h} fps: {fps} time: {time.strftime("%H:%M:%S", time.localtime())}',
                (0, h - 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
            cv2.imshow("cam", frame)
            vid_writer.write(frame)
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyWindow("cam")
                msg.showinfo(title="Успех", message=f'Запись сохранена в {dest_path} .')
                self._rec_btn.config(state='disabled')  
                break
    
                
class Task8(main.TaskFrame):
    '''Лаб 1. Задание 8'''
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        ttk.Label(
            self._main_frame,
            text="Веб-камера с цветочувствительным центром"
        ).pack(expand=True)
        
        ttk.Button(
            self._main_frame,
            text='Показать видео',
            command=self._show_cam
        ).pack(expand=True)
        
    @staticmethod
    def round_color(color: Iterable[int]):
        b, g, _ = color
        _max = max(color)
        if _max == b:
            return (255, 0, 0)
        elif _max == g: 
            return (0, 255, 0)
        else:
            return (0, 0, 255)
    
    def _show_cam(self) -> None:
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("cam", cv2.WINDOW_AUTOSIZE)
        
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        width = 40

        top_left_1: tuple[int, int] = (w//2 - width//2, width//2)
        bottom_right_1: tuple[int, int] = (w//2 + width//2, h - width//2)

        top_left_2: tuple[int, int] = (width//2, h//2 - width//2)
        bottom_right_2: tuple[int, int] = (w - width//2, h//2 + width//2)

        while cap.grab():
            frame = cap.read()[1]
            
            center_pixel = frame[w//2, h//2]
            color = self.round_color(center_pixel)

            frame = cv2.rectangle(frame, top_left_1, bottom_right_1, color, 2)
            frame = cv2.rectangle(frame, top_left_2, bottom_right_2, color, 2)
            cv2.imshow("cam", frame)
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyWindow("cam")
                break
            

class Task9(main.TaskFrame):
    '''Лаб 1. Задание 9'''
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        self._main_frame.rowconfigure(index=(0, 2), weight=1)
        self._main_frame.rowconfigure(index=1, weight=2)
        self._main_frame.columnconfigure(index=(0,1,2), weight=1)
        
        ttk.Label(
            self._main_frame,
            text="Трансляция с ip-камеры"
        ).grid(row=0, column=0, columnspan=3)
            
        ttk.Label(
            self._main_frame,
            text="Введите ip-адрес камеры:"
        ).grid(row=1, column=0)
        
        self._ip_var = tk.StringVar(value="")
        
        ttk.Entry(
            self._main_frame,
            textvariable=self._ip_var
        ).grid(row=1, column=1, columnspan=2)
        
        ttk.Button(
            self._main_frame,
            text='Открыть камеру',
            command=self._show_cam
        ).grid(row=2, column=0, columnspan=3)
    
    def _show_cam(self) -> None:
        if (ip:=self._ip_var.get()) != "":
            Task3.play_video(ip)
        else:
            msg.showwarning(
                title="Не найдена камера",
                message="Камера с таким ip не найдена, проверьте подключение и повторите попытку."
            )
    