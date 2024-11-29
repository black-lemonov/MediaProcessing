import tkinter.filedialog as fd
import cv2

from canny import director


def main() -> None:
    img_path = fd.askopenfilename(
        title='Выберите изображение:',
        initialdir="/home/egorp/Изображения",
        filetypes=(('',".png .jpg .jpeg .ico"),)
    )
    img = cv2.imread(img_path)
    cv2.namedWindow("Исходное изображение")
    cv2.imshow('Исходное изображение', img)
    
    edges = director.sobel().detect(img)
    cv2.namedWindow("Алгоритм Канни")
    cv2.imshow("Алгоритм Канни", edges)
    
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
    


if __name__ == "__main__":
    main()