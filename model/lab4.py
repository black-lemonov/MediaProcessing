import cv2


def task1(img_path: str) -> None:
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow("orig")
    cv2.namedWindow("blur")
    cv2.imshow("orig", img)
    cv2.imshow(
        "blur",
        cv2.GaussianBlur(
            img, (5,5), 3
        )
    )
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        
task1("путь к изображению")
