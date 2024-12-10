from tkinter import filedialog as fd

import cv2


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