from tkinter import filedialog as fd

import cv2
import numpy as np


def wb_blur(frame: np.ndarray):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5,5), 0)
    return frame


def motion_detection() -> None:
    src_path = fd.askopenfilename(
        title='Выберите изображение:',
        initialdir="/home/egorp/Видео",
        filetypes=(('', ".mp4"),)
    )

    video = cv2.VideoCapture(src_path)
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')


if __name__ == '__main__':
    motion_detection()