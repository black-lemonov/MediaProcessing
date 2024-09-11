import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd  
from tkinter import messagebox as msg

from overrides import override
import cv2

import main


class Task2(main.TaskFrame):
    '''Лаба 1. Задание 2.
    Открытие фото в окнах разных размеров
    и с разными цвето-фильтрами.'''
    @override
    def __init__(self, nbook: ttk.Notebook, title: str) -> None:
        self._set_filters()
        self._set_sizes()
        super().__init__(nbook, title)
        
    def _set_filters(self) -> None:
        self._filters: dict[str, int] = {
            'оригинальный': cv2.IMREAD_UNCHANGED,
            'серый': cv2.IMREAD_GRAYSCALE,
            'RGB': cv2.IMREAD_COLOR,
        }
        
    def _set_sizes(self) -> None:
        self._win_sizes: dict[str, int] = {
            'нормальный': cv2.WINDOW_NORMAL,
            'авто': cv2.WINDOW_AUTOSIZE,
            'полный экран': cv2.WINDOW_FULLSCREEN,
            'те же пропорции': cv2.WINDOW_FREERATIO
        }
    
    @override
    def _set_task(self) -> None:
        btns_frame = ttk.Frame(self._root)
        btns_frame.pack(expand=True, fill='x')
        
        btns_frame.rowconfigure(index=0, weight=1)
        btns_frame.columnconfigure(index=(0,1), weight=1)
        
        ttk.Button(
            btns_frame,
            text='Выбрать фото...',
            command=self._set_filepath
        ).grid(row=0, column=0)
        
        ttk.Button(
            btns_frame,
            text='Показать...',
            state='normal',
            command=self._show_photo
        ).grid(row=0, column=1)
        
        boxes_frame = ttk.Frame(self._root)
        boxes_frame.pack(expand=True, fill='x')
        
        boxes_frame.rowconfigure(index=0, weight=1)
        boxes_frame.columnconfigure(index=(0, 1), weight=1)
        
        filters = tuple(self._filters.keys())
        self._filter_var = tk.StringVar(value=filters[0])
        ttk.Combobox(
            boxes_frame,
            values=filters,
            textvariable=self._filter_var,
            state='readonly'
        ).grid(row=0, column=0)
        
        sizes = tuple(self._win_sizes.keys())
        self._size_var = tk.StringVar(value=sizes[0])
        ttk.Combobox(
            boxes_frame,
            values=sizes,
            textvariable=self._size_var,
            state='readonly'
        ).grid(row=0, column=1)
        
    def _set_filepath(self) -> None:
        self._filepath = fd.askopenfilename()
        
    def _show_photo(self) -> None:
        photo = self._filepath
        size = self._win_sizes[self._size_var.get()]
        color = self._filters[self._filter_var.get()]
        
        try:
            cv2.namedWindow(photo, size) 
        except KeyError:
            print(
                f'''Неизвестный размер: {size}.
                Доступные размеры: {', '.join(self._win_sizes.keys())} .'''
            )
        
        photo_matr = cv2.imread(photo, color)
        
        try:
            cv2.imshow(photo, photo_matr)
        except KeyError:
            print(
                f'''Неизвестный цвет: {color}.
                Доступные размеры: {', '.join(self._filters.keys())} .'''
            )
            
        if cv2.waitKey() == 27:
            cv2.destroyAllWindows()
            return 


class Task3(main.TaskFrame):
    '''Лаб 1. Задание 3. Открытие видео с разными фильтрами.'''    
    @override
    def __init__(self, nbook: ttk.Notebook, title: str) -> None:
        self._set_filters()
        self._set_sizes()
        super().__init__(nbook, title)
    
    def _set_filters(self) -> None:
        self._filters: dict[str, int] = {
            'gray': cv2.COLOR_BGR2GRAY,
            'blue': cv2.COLOR_BGRA2RGBA,
            'colored': cv2.COLOR_RGB2RGBA,
            'vapor': cv2.COLOR_BGR2LUV  
        }
        
    def _set_sizes(self) -> None:
        self._win_sizes: dict[str, int] = {
            'нормальный': cv2.WINDOW_NORMAL,
            'авто': cv2.WINDOW_AUTOSIZE,
            'полный экран': cv2.WINDOW_FULLSCREEN,
            'те же пропорции': cv2.WINDOW_FREERATIO
        }
    
    @override
    def _set_task(self) -> None:
        btns_frame = ttk.Frame(self._root)
        btns_frame.pack(expand=True, fill='x')
        
        btns_frame.rowconfigure(index=0, weight=1)
        btns_frame.columnconfigure(index=(0,1), weight=1)
        
        ttk.Button(
            btns_frame,
            text='Выбрать видео...',
            command=self._set_filepath
        ).grid(row=0, column=0)
        
        ttk.Button(
            btns_frame,
            text='Смотреть...',
            state='normal',
            command=self._play_video
        ).grid(row=0, column=1)
        
        boxes_frame = ttk.Frame(self._root)
        boxes_frame.pack(expand=True, fill='x')
        
        boxes_frame.rowconfigure(index=0, weight=1)
        boxes_frame.columnconfigure(index=(0, 1), weight=1)
        
        filters = tuple(self._filters.keys())
        self._filter_var = tk.StringVar(value=filters[0])
        ttk.Combobox(
            boxes_frame,
            values=filters,
            textvariable=self._filter_var,
            state='readonly'
        ).grid(row=0, column=0)
        
        sizes = tuple(self._win_sizes.keys())
        self._size_var = tk.StringVar(value=sizes[0])
        ttk.Combobox(
            boxes_frame,
            values=sizes,
            textvariable=self._size_var,
            state='readonly'
        ).grid(row=0, column=1)
        
    def _set_filepath(self) -> None:
        self._filepath = fd.askopenfilename()
    
    def _play_video(self) -> None:
        video = self._filepath
        size = self._win_sizes[self._size_var.get()]
        color = self._filters[self._filter_var.get()]
        
        cap = cv2.VideoCapture(video, cv2.CAP_ANY)
        
        if not cap.isOpened():
            return
        
        while cap.grab():
            is_ok, frame = cap.read()
            if not is_ok:
                break      
            try:
                filtered_frame = cv2.cvtColor(
                    frame, color
                )
            except KeyError:
                print(
                    f'''Неизвестный фильтр: {color}.
                    Доступные фильтры: {', '.join(self._filters.keys())} .'''
                )
            
            cv2.imshow(video, filtered_frame)
            
            if cv2.waitKey(10) == 27:
                cv2.destroyAllWindows()
                break
            
        cap.release()
        cv2.destroyAllWindows()


class Task4(main.TaskFrame):
    '''Задание 4. Записывает видео из файла в другой файл'''
    @override
    def _set_task(self) -> None:
        
        main_frame = ttk.Frame(self._root)
        main_frame.pack(expand=True, fill='both')
        main_frame.rowconfigure(index=(0,1), weight=1)
        main_frame.columnconfigure(index=(0,2), weight=1)
        main_frame.columnconfigure(index=1, weight=2)
        
        ttk.Label(
            main_frame,
            width=15,
            text='Сохранить как:'
        ).grid(row=0, column=0)
        
        self._destpath_var = tk.StringVar(value='')
        
        ttk.Entry(
            main_frame,
            textvariable=self._destpath_var,
            width=25,
        ).grid(row=0, column=1)
        
        ttk.Button(
            main_frame,
            text='*',
            width=5,
            command=self._set_dest_dir
        ).grid(row=0, column=2)
        
        ttk.Button(
            main_frame,
            text='Выбрать видео...',
            command=self._set_srcpath
        ).grid(row=1, column=0)
        
        ttk.Button(
            main_frame,
            text='Сохранить',
            state='normal',
            command=self._rewrite_video
        ).grid(row=1, column=2)
    
    def _set_dest_dir(self) -> None:
        self._destpath_var.set(fd.askdirectory() + '/')
        
    def _set_srcpath(self) -> None:
        self._srcpath = fd.askopenfilename()
        
    def _rewrite_video(self) -> None:        
        src = self._srcpath
        dest = self._destpath_var.get()
        
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
    