import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd  
from tkinter import messagebox as msg

from overrides import override
from ffpyplayer.player import MediaPlayer
import cv2

import main


class Task2(main.TaskFrame):
    '''Лаба 1. Задание 2.
    Открытие фото в окнах разных размеров
    и с разными цвето-фильтрами.'''
    
    def _set_filters_frame(self) -> None:
        self._filters: dict[str, int] = {
            'оригинальный': cv2.IMREAD_UNCHANGED,
            'серый': cv2.IMREAD_GRAYSCALE,
            'RGB': cv2.IMREAD_COLOR,
        }
        self._filter_var = tk.IntVar(value=cv2.IMREAD_UNCHANGED)
        self._filters_frame = ttk.Frame(self._main_frame)

        ttk.Label(self._filters_frame, text='Фильтры:').pack(expand=True, fill='x')
        
        for k, v in self._filters.items():
            ttk.Radiobutton(
                self._filters_frame,
                text=k,
                value=v,
                variable=self._filter_var
            ).pack(expand=True, fill='x')
            
    def _set_sizes_frame(self) -> None:
        self._win_sizes: dict[str, int] = {
            'нормальный': cv2.WINDOW_NORMAL,
            'полный экран': cv2.WINDOW_FULLSCREEN,
            'те же пропорции': cv2.WINDOW_FREERATIO
        }
        self._size_var = tk.IntVar(value=cv2.WINDOW_NORMAL)
        self._sizes_frame = ttk.Frame(self._main_frame)

        ttk.Label(self._sizes_frame, text='Размеры:').pack(expand=True, fill='x')
        
        for k, v in self._win_sizes.items():
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
        
        self._main_frame.rowconfigure(index=0, weight=2)
        self._main_frame.rowconfigure(index=1, weight=1)
        self._main_frame.columnconfigure(index=(0, 1), weight=1)
                
        self._set_filters_frame()
        self._filters_frame.grid(row=0, column=0)
        
        self._set_sizes_frame()
        self._sizes_frame.grid(row=0, column=1)
        
        ttk.Button(
            self._main_frame,
            text='Выбрать фото...',
            command=self._set_filepath
        ).grid(row=1, column=0)
        
        self._open_btn = ttk.Button(
            self._main_frame,
            text='Открыть',
            state='disabled',
            command=self._show_photo
        )
        self._open_btn.grid(row=1, column=1)
        
    def _set_filepath(self) -> None:
        self._filepath = fd.askopenfilename(
            title='Выберите фотографию:',
            initialdir=r'D:\Media\pics'
        )
        if len(self._filepath) > 0:
            self._open_btn.config(state='normal')
        
    def _show_photo(self) -> None:        
        size = self._size_var.get()
        color = self._filter_var.get()
        photo = self._filepath
        
        photo_matr = cv2.imread(photo, color)
        cv2.namedWindow(photo, size) 
        cv2.imshow(photo, photo_matr)
        
        if cv2.waitKey(0) == 27:
            cv2.destroyAllWindows()
            return 


class Task3(main.TaskFrame):
    '''Лаб 1. Задание 3. Открытие видео с разными фильтрами.'''    
    def _set_filters_frame(self) -> None:
        self._filters: dict[str, int] = {
            'RGBA': cv2.COLOR_RGB2RGBA,
            'GRAY': cv2.COLOR_BGR2GRAY,
            'BGRA': cv2.COLOR_BGRA2RGBA,
            'BGRA LUV': cv2.COLOR_BGR2LUV  
        }
        self._filter_var = tk.IntVar(value=cv2.COLOR_RGB2RGBA)
        self._filters_frame = ttk.Frame(self._main_frame)

        ttk.Label(self._filters_frame, text='Цвета:').pack(expand=True, fill='x')
        
        for k, v in self._filters.items():
            ttk.Radiobutton(
                self._filters_frame,
                text=k,
                value=v,
                variable=self._filter_var
            ).pack(expand=True, fill='x')
            
    def _set_sizes_frame(self) -> None:
        self._win_sizes: dict[str, int] = {
            'нормальный': cv2.WINDOW_NORMAL,
            'полный экран': cv2.WINDOW_FULLSCREEN,
            'те же пропорции': cv2.WINDOW_FREERATIO
        }
        self._size_var = tk.IntVar(value=cv2.WINDOW_NORMAL)
        self._sizes_frame = ttk.Frame(self._main_frame)

        ttk.Label(self._sizes_frame, text='Размеры:').pack(expand=True, fill='x')
        
        for k, v in self._win_sizes.items():
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
        
        self._main_frame.rowconfigure(index=0, weight=2)
        self._main_frame.rowconfigure(index=1, weight=1)
        self._main_frame.columnconfigure(index=(0, 1), weight=1)
                
        self._set_filters_frame()
        self._filters_frame.grid(row=0, column=0)
        
        self._set_sizes_frame()
        self._sizes_frame.grid(row=0, column=1)
        
        ttk.Button(
            self._main_frame,
            text='Выбрать видео...',
            command=self._set_filepath
        ).grid(row=1, column=0)
        
        self._play_btn = ttk.Button(
            self._main_frame,
            text='Открыть',
            state='disabled',
            command=self._play_video
        )
        self._play_btn.grid(row=1, column=1)
        
    def _set_filepath(self) -> None:
        self._filepath = fd.askopenfilename(
            title='Выберите фотографию:',
            initialdir=r'D:\Media\vids'
        )
        if len(self._filepath) > 0:
            self._play_btn.config(state='normal')
    
    def _play_video(self) -> None:
        video = self._filepath
        size = self._size_var.get()
        color = self._filter_var.get()
        fps = 60
        
        cap = cv2.VideoCapture(video, cv2.CAP_ANY)
        player = MediaPlayer(video)
        if not cap.isOpened():
            return
        
        while cap.grab():
            is_ok, frame = cap.read()
            audio_frame, val = player.get_frame()
            if not is_ok:
                break      
            try:
                filtered_frame = cv2.cvtColor(frame, color)
            except KeyError:
                print(
                    f'''Неизвестный фильтр: {color}.
                    Доступные фильтры: {', '.join(self._filters.keys())} .'''
                )
            
            cv2.imshow(video, filtered_frame)
            
            if cv2.waitKey(fps) == 27:
                break
            
        cap.release()
        cv2.destroyAllWindows()


class Task4(main.TaskFrame):
    '''Задание 4. Записывает видео из файла в другой файл'''
    @override
    def _set_task(self) -> None:
        self._main_frame = ttk.Frame(self._root)
        self._main_frame.pack(expand=True, fill='both')
        
        self._choose_btn = ttk.Button(
            self._main_frame,
            text='Выбрать файл',
            command=self._set_src_path
        )
        self._choose_btn.pack(expand=True)
        
        self._save_btn = ttk.Button(
            self._main_frame,
            text='Сохранить как',
            state='disabled',
            command=self._save_video
        )
        self._save_btn.pack(expand=True)

    def _set_src_path(self) -> None:
        self._src_path = fd.askopenfilename(
            title='Выбор видео...',
            defaultextension='.mp4',
            initialdir=r'D:\Media\vids'
        )
        if len(self._src_path) > 0:
            self._save_btn.config(state='normal')
        
    def _save_video(self) -> None:        
        src = self._src_path
        dest = fd.asksaveasfilename(
            title='Копирование...',
            initialdir=r'D:\Media\vids',
            initialfile='копия_без_звука.mp4',
            defaultextension='.mp4',
            confirmoverwrite=True
        )
        if len(dest) == 0:
            return
        
        self._choose_btn.config(state='disabled')
        self._save_btn.config(state='disabled')
        self._main_frame.update()
        
        vid_reader = cv2.VideoCapture(src)
        
        if not vid_reader.isOpened():
            msg.showerror(title="Ошибка", message="Видео не было открыто. Проверьте путь к источнику.")
            return
        
        w = int(vid_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(vid_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        vid_writer = cv2.VideoWriter(dest, fourcc, 15, (w, h))
        
        if not vid_writer.isOpened():
            msg.showerror(title="Ошибка", message="Файл назначения не был создан. Проверьте путь назначения.")
            return
        
        is_ok, frame = vid_reader.read()
        
        while is_ok:
            vid_writer.write(frame)
            is_ok, frame = vid_reader.read()
        
        vid_reader.release()
        vid_writer.release()
        msg.showinfo(title="Успех", message=f'Видео успешно сохранено в: {dest} .')
        self._choose_btn.config(state='normal')
        self._save_btn.config(state='normal')     
    