'''Функция с заданиями к лаб1'''

from typing import Literal, Iterable
from tkinter import messagebox as msg
import time

import cv2

CV_COLOR_SPACES: dict[Literal["BGRA", "GRAY", "LUV", "HLS", "HSV", "YCrCb", "YUV"], int] = {
    "BGRA": cv2.COLOR_BGR2BGRA,
    "GRAY": cv2.COLOR_BGR2GRAY,
    "LUV": cv2.COLOR_BGR2LUV,
    "HLS": cv2.COLOR_BGR2HLS,
    "HSV": cv2.COLOR_BGR2HSV,
    "YCrCb": cv2.COLOR_BGR2YCrCb,
    "YUV": cv2.COLOR_BGR2YUV,
}

CV_WINDOW_FLAGS: dict[Literal["NORMAL", "FULLSCREEN", "KEEPRATIO"], int] = {
    "NORMAL": cv2.WINDOW_GUI_NORMAL,
    "FULLSCREEN": cv2.WINDOW_FULLSCREEN,
    "KEEPRATIO": cv2.WND_PROP_ASPECT_RATIO
}

def show_image(path: str,
               win_title: str = 'image',
               win_flag: int = cv2.WINDOW_NORMAL,
               color_space: int = cv2.COLOR_BGR2BGRA) -> None:
    '''Создает окно с изображением'''        
    frame = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    cv2.namedWindow(win_title, win_flag) 
    frame = cv2.cvtColor(frame, color_space)
    cv2.imshow(win_title, frame)


def move_window(win_title: str, x: int, y: int):
    cv2.moveWindow(win_title, x, y)


def close_window(win_title: str, key: int = 27):
    if cv2.waitKey(0) == key:
        cv2.destroyWindow(win_title)
        
        
def close_all(key: int = 27):
    if cv2.waitKey(0) == key:
        cv2.destroyAllWindows()
        
        
def play_video(path: str,
               win_title: str = 'video',
               win_flag: int = cv2.WINDOW_NORMAL,
               color_space: int = cv2.COLOR_BGR2RGBA) -> None:
    cap = cv2.VideoCapture(path)
    
    if not cap.isOpened():
        return
    
    cv2.namedWindow(win_title, win_flag)        
    while True:
        grabbed, frame = cap.read()
        if not grabbed:
            break
        colored_frame = cv2.cvtColor(frame, color_space)
        cv2.imshow(win_title, colored_frame)
        if cv2.waitKey(70) == 27:
            break
    cap.release()
    cv2.destroyWindow(win_title)
    

def save_video(src_path: str, dest_path: str) -> None:        
    vid_reader = cv2.VideoCapture(src_path)
    
    if not vid_reader.isOpened():
        msg.showerror(
            title="Ошибка",
            message="Видео не было открыто. Проверьте путь к источнику."
        )
        return
    
    w = int(vid_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(vid_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps= float(vid_reader.get(cv2.CAP_PROP_FPS))
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    
    vid_writer = cv2.VideoWriter(dest_path, fourcc, fps, frameSize=(w, h))
    
    if not vid_writer.isOpened():
        msg.showerror(
            title="Ошибка",
            message="Файл назначения не был создан. Проверьте путь назначения."
        )
        return
    
    while True:
        grabbed, frame = vid_reader.read()
        if not grabbed:
            break
        vid_writer.write(frame)
    
    vid_reader.release()
    vid_writer.release()
    msg.showinfo(
        title="Успех",
        message=f'Видео успешно сохранено в: {dest_path} .'
    )  
    

def show_cam() -> None:
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
        

def record_cam(dest_path: str) -> None:
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
            break
        

def round_color(color: Iterable[int]):
    b, g, _ = color
    _max = max(color)
    if _max == b:
        return (255, 0, 0)
    elif _max == g: 
        return (0, 255, 0)
    else:
        return (0, 0, 255)
        
        
def show_cam2() -> None:
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
        color = round_color(center_pixel)

        frame = cv2.rectangle(frame, top_left_1, bottom_right_1, color, 2)
        frame = cv2.rectangle(frame, top_left_2, bottom_right_2, color, 2)
        cv2.imshow("cam", frame)
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyWindow("cam")
            break
        