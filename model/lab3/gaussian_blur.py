from typing import Sequence
import tkinter.filedialog as fd

import cv2
import numpy as np
from progress.bar import Bar


def _print_mat(matlike, size: int, acc: int = 2) -> None:
    """Вывод квадратных матриц

    Args:
        matlike (NDArray): матрица
        size (int): размер матрицы
        acc (int, optional): точность (знаков после запятой). По умолчанию 2.
    """
    for i in range(size):
        for j in range(size):
            print(f"{matlike[i, j]:.{acc}f}", end='\t')
        print()


def gauss(x: int, y: int, sigma: float, mu_x: float, mu_y: float) -> float:
    """Функция Гаусса от 2 переменных

    Args:
        x (int): координата x
        y (int): координата y
        sigma (float): средн отклонение
        mu_x (float): мат ожидание для x
        mu_y (float): мат ожидание для y

    Returns:
        float: значение функции
    """
    return 1 / (2 * np.pi * sigma ** 2) * np.e ** (-((x-mu_x)**2 + (y-mu_y)**2)/(2*sigma**2))

    
def gauss_kernel(ksize: int, sigma: float, mu_x: float, mu_y: float | None = None):
    """Ядро Гауссовой свёртки

    Args:
        ksize (int): размер ядра
        sigma (float): сред отклонение для функции Гаусса
        mu_x (float): мат ожидание для x для функции Гаусса
        mu_y (float | None, optional): мат ожидание для y для функции Гаусса. Если None, то равно mu_x.

    Raises:
        ValueError: если размер ядра отрицательный или четный

    Returns:
        NDArray[float64]: ядро свёртки
    """
    if ksize < 0 or ksize % 2 == 0:
        raise ValueError("Ошибка: размер ядра должен быть положительным нечетным числом!")
    if mu_y is None:
        mu_y = mu_x
    kernel = np.empty((ksize, ksize))
    for i in range(ksize):
        for j in range(ksize):
            kernel[i, j] = gauss(i, j, sigma, mu_x, mu_y)
    return kernel / np.sum(kernel)


def apply_convolution(img, kernel, ksize: int) -> None:
    """Применение свертки к внутренним пикселям изображения

    Args:
        img (MatLike): матрица изображения
        kernel (NDArray): ядро свертки
        ksize (int): размер ядра

    Returns:
        MatLike: изображение-результат применения свёртки 
    """
    w, h = img.shape[0], img.shape[1]
    w, h = h, w
    margin = ksize // 2
    blurred = np.zeros((h-margin*2, w-margin*2, 3), np.uint8)
    
    progress_bar = Bar(
        "Свёртка изображения...", 
        max=(h-2*margin)*(w-2*margin),
        suffix="%(percent)d%%"
    )
    
    for y in range(margin, h - margin):
        for x in range(margin, w - margin):
            b = g = r = 0 
            for y0 in range(y - margin, y + margin + 1):
                for x0 in range(x - margin, x + margin + 1):
                    img_bgr = img[y0, x0]
                    kernel_val = kernel[y0-(y-margin)][x0-(x-margin)]
                    b += img_bgr[0] * kernel_val
                    g += img_bgr[1] * kernel_val
                    r += img_bgr[2] * kernel_val
            blurred[y-margin, x-margin] = (b,g,r)
            
            progress_bar.next()
    progress_bar.finish()
    
    return blurred


def apply_convolution_gray(gray_img: np.ndarray, kernel: Sequence[Sequence], ksize: int):
    w, h = gray_img.shape[0], gray_img.shape[1]
    w, h = h, w
    margin = ksize // 2
    result = np.zeros((h-margin*2, w-margin*2), np.int32)
    
    for y in range(margin, h - margin):
        for x in range(margin, w - margin):
            val = 0 
            for y0 in range(y - margin, y + margin + 1):
                for x0 in range(x - margin, x + margin + 1):
                    img_val = gray_img[y0, x0]
                    kernel_val = kernel[y0-(y-margin)][x0-(x-margin)]
                    val += img_val * kernel_val
            result[y-margin, x-margin] = val
    
    return result


def main(img_path: str, ksize: int, sigma: float) -> None:
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    kernel = gauss_kernel(ksize, sigma, ksize // 2)
    blurred = apply_convolution(img, kernel, ksize)
    # blurred = cv2.GaussianBlur(img, (ksize, ksize), sigma)
    
    cv2.namedWindow("original")
    cv2.imshow("original", img)
    cv2.namedWindow("blurred")
    cv2.imshow("blurred", blurred)
    cv2.moveWindow("blurred", max(img.shape), 100)
    
    if cv2.waitKey(0) != 27:
        cv2.destroyWindow("blurred")
    

if __name__ == "__main__":
    img_path = fd.askopenfilename(
        title='Выберите изображение:',
        initialdir="/home/egorp/Изображения",
        filetypes=(('',".png .jpg .jpeg .ico"),)
    )
    if len(img_path) > 0:
        main(img_path, ksize=9, sigma=1)
