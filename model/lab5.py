import cv2
import numpy as np


def wb_blur(frame: np.ndarray):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5,5), 0)
    return frame


def motion_detection() -> None:
    thresh = 32
    min_area = 20

    src_path = "/home/egorp/Видео/ЛР5_видео/archive/ЛР4_main_video.mov"

    video = cv2.VideoCapture(src_path)
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')

    grabbed, frame_prev = video.read()
    if not grabbed:
        return

    frame_prev = wb_blur(frame_prev)

    dest_path = "/home/egorp/Видео/ЛР5_видео/LR5_motion.mp4"

    video_writer = cv2.VideoWriter(dest_path, fourcc, fps, (w, h))

    while True:
        grabbed, frame_raw = video.read()
        if not grabbed:
            break

        frame = wb_blur(frame_raw)
        frame_diff = cv2.absdiff(frame_prev, frame)
        _, frame_threshold = cv2.threshold(frame_diff, thresh, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if any([cv2.contourArea(cnt) > min_area for cnt in contours]):
            video_writer.write(frame_raw)

        cv2.imshow("original", frame_raw)
        frame_prev = frame

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

    video.release()
    video_writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    motion_detection()