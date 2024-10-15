from typing import override

import cv2


class Task1:
    def main(self) -> None:
        '''
        Читает изображение с камеры и переводит его в формат HSV.
        После перевода в HSV осуществляет преобразования с изображением при
        помощи методов hook. 
        '''
        self._cam = cv2.VideoCapture(0)
        self._winname = "cam"
        cv2.namedWindow(winname=self._winname)
        self.hook1()
        while True:
            grabbed, self._frame = self._cam.read()
            if not grabbed:
                break
            self._frame = cv2.cvtColor(
                src=self._frame,
                code=cv2.COLOR_BGR2HSV_FULL
            )
            self.hook2()
            cv2.imshow(
                winname=self._winname,
                mat=self._frame
            )
            if cv2.waitKey(1) == 27:
                self._cam.release()
                cv2.destroyAllWindows()
    
    def hook1(self) -> None:
        '''Пустая реализация, возможность для создания ползунков'''
        pass
    
    def hook2(self) -> None:
        '''Пустая реализация, возможность для фильтрации изображения'''
        pass
    
    def hook3(self) -> None:
        '''Возможно моменты изображения'''
        pass
    

class Task2(Task1):
    @override
    def hook1(self) -> None:
        '''Ползунки'''
        self._low_h: int = 0
        self._low_s: int = 0 # 0..255
        self._low_v: int = 0 # 0..255
        self._high_h: int = 180
        self._high_s: int = 255 # 0..255
        self._high_v: int = 255 # 0..255
        cv2.createTrackbar(
            "H low",
            self._winname,
            0, 255,
            self._ch_low_h
        )
        cv2.createTrackbar(
            "S low",
            self._winname,
            0, 255,
            self._ch_low_s
        )
        cv2.createTrackbar(
            "V low",
            self._winname,
            0, 255,
            self._ch_low_v
        )
        cv2.createTrackbar(
            "H high",
            self._winname,
            255, 255,
            self._ch_high_h
        )
        cv2.createTrackbar(
            "S high",
            self._winname,
            255, 255,
            self._ch_high_s
        )
        cv2.createTrackbar(
            "V high",
            self._winname,
            255, 255,
            self._ch_high_v
        )
    
    def _ch_low_h(self, val: int) -> None:
        self._low_h = val
        cv2.setTrackbarPos("H low", self._winname, val)
    
    def _ch_low_s(self, val: int) -> None:
        self._low_s = val
        cv2.setTrackbarPos("S low", self._winname, val)
        
    def _ch_low_v(self, val: int) -> None:
        self._low_v = val
        cv2.setTrackbarPos("V low", self._winname, val)
        
    def _ch_high_h(self, val: int) -> None:
        self._high_h = val
        cv2.setTrackbarPos("H high", self._winname, val)
    
    def _ch_high_s(self, val: int) -> None:
        self._high_s = val
        cv2.setTrackbarPos("S high", self._winname, val)
        
    def _ch_high_v(self, val: int) -> None:
        self._high_v = val
        cv2.setTrackbarPos("V high", self._winname, val)
    
    @override
    def hook2(self) -> None:
        '''Фильтрация изображения'''
        hsv_low = (self._low_h, self._low_s, self._low_v)
        hsv_high = (self._high_h, self._high_s, self._high_v)
        self._red_mask = cv2.inRange(self._frame, hsv_low, hsv_high)
        self._frame = cv2.bitwise_and(
            self._frame,
            self._frame,
            mask=self._red_mask
        )
        self.hook3()
        
    def hook3(self) -> None:
        '''Место для морфологических преобразований'''
        pass
    


class Task3(Task2):
    @override
    def hook1(self):
        super().hook1()
        cv2.namedWindow(winname="opening")
        cv2.namedWindow(winname="closing")
    
    @override
    def hook3(self) -> None:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        self._opening_mask = cv2.morphologyEx(
            src=self._red_mask,
            op=cv2.MORPH_OPEN,
            kernel=kernel
        )
        opening_frame = cv2.bitwise_and(
            self._frame,
            self._frame,
            mask=self._opening_mask
        )
        self.hook4()
        cv2.imshow(
            winname="opening",
            mat=opening_frame
        )
        self._closing_mask = cv2.morphologyEx(
            src=self._red_mask,
            op=cv2.MORPH_CLOSE,
            kernel=kernel
        )
        closing_frame = cv2.bitwise_and(
            self._frame,
            self._frame,
            mask=self._closing_mask
        )
        self.hook5()
        cv2.imshow(
            winname="closing",
            mat=closing_frame
        )
    
    def hook4(self) -> None:
        '''Моменты для открытия'''
        pass
    
    def hook5(self) -> None:
        '''Моменты для закрытия'''
        pass
            

class Task4(Task3):
    @override
    def hook4(self) -> None:
        moments = cv2.moments(self._opening_mask, True)
        self._m00 = moments["m00"]
        self._m10 = moments["m10"]
        self._m01 = moments["m01"]
    
    @override
    def hook5(self) -> None:
        moments = cv2.moments(self._closing_mask, True)
        self._m00 = moments["m00"]
        self._m10 = moments["m10"]
        self._m01 = moments["m01"]
        

class Task5(Task2):
    def hook3(self):
        '''Построение цветного прямоугольника вокруг объекта'''
        x, y, w, h = cv2.boundingRect(self._red_mask)
        self._frame = cv2.rectangle(self._frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
    

if __name__ == "__main__":
    Task3().main()