from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import cv2
import numpy as np
import win32gui
from PIL import ImageGrab , Image
import serial.tools.list_ports
import serial.tools.list_ports
import threading
import serial
import struct
import ctypes
import win32api
import sys

form_class = uic.loadUiType("mainWindow.ui")[0]
print(cv2.__file__)
#메이플 x, y , w , h , hwnd
global mapleOn
mapleOn = 0,0,0,0,0

# 미니맵 x, y , w, h ,적중률 왼위 오른아래
global miniMap
miniMap = 0,0,0,0,0,0

# [0] 내위치 X [1] 내위치 Y
global stat
stat = 0 , 0
# 룬 [0,1] 위치 xy [2] 룬 여부 [3] 룬체크 0은 체크함 1은 체크안함
global rune
rune = 0, 0, 0, 0
# 무한반복 0 은 반복함 1은 반복안함
global inficheck
inficheck = 0


# 키마 세팅 클래스
class keymouse():

    # Mouse basic commands and arguments
    MOUSE_CMD            = 0xE0
    MOUSE_CALIBRATE      = 0xE1
    MOUSE_PRESS          = 0xE2
    MOUSE_RELEASE        = 0xE3

    MOUSE_CLICK          = 0xE4
    MOUSE_FAST_CLICK     = 0xE5
    MOUSE_MOVE           = 0xE6
    MOUSE_BEZIER         = 0xE7

    # Mouse buttons
    MOUSE_LEFT           = 0xEA
    MOUSE_RIGHT          = 0xEB
    MOUSE_MIDDLE         = 0xEC
    MOUSE_BUTTONS        = [MOUSE_LEFT,
                            MOUSE_MIDDLE,
                            MOUSE_RIGHT]

    # Keyboard commands and arguments
    KEYBOARD_CMD         = 0xF0
    KEYBOARD_PRESS       = 0xF1
    KEYBOARD_RELEASE     = 0xF2
    KEYBOARD_RELEASE_ALL = 0xF3
    KEYBOARD_PRINT       = 0xF4
    KEYBOARD_PRINTLN     = 0xF5
    KEYBOARD_WRITE       = 0xF6
    KEYBOARD_TYPE        = 0xF7

    # Arduino keyboard modifiers
    # http://arduino.cc/en/Reference/KeyboardModifiers
    LEFT_CTRL            = 0x80
    LEFT_SHIFT           = 0x81
    LEFT_ALT             = 0x82
    LEFT_GUI             = 0x83
    RIGHT_CTRL           = 0x84
    RIGHT_SHIFT          = 0x85
    RIGHT_ALT            = 0x86
    RIGHT_GUI            = 0x87
    UP_ARROW             = 0xDA
    DOWN_ARROW           = 0xD9
    LEFT_ARROW           = 0xD8
    RIGHT_ARROW          = 0xD7
    BACKSPACE            = 0xB2
    TAB                  = 0xB3
    RETURN               = 0xB0
    ESC                  = 0xB1
    INSERT               = 0xD1
    DELETE               = 0xD4
    PAGE_UP              = 0xD3
    PAGE_DOWN            = 0xD6
    HOME                 = 0xD2
    END                  = 0xD5
    CAPS_LOCK            = 0xC1
    F1                   = 0xC2
    F2                   = 0xC3
    F3                   = 0xC4
    F4                   = 0xC5
    F5                   = 0xC6
    F6                   = 0xC7
    F7                   = 0xC8
    F8                   = 0xC9
    F9                   = 0xCA
    F10                  = 0xCB
    F11                  = 0xCC
    F12                  = 0xCD

    # etc.
    SCREEN_CALIBRATE     = 0xFF
    COMMAND_COMPLETE     = 0xFE


# 아두이노 제어 클래스
class Arduino(object):

    def __init__(self, port=None, baudrate=115200):
        """
        Args:
          port (str, optional): Device name or port number number or None.
          baudrate (str, optional): Baud rate such as 9600 or 115200 etc.
        Raises:
          SerialException: In the case the device cannot be found.
        Note:
          You should not have to specify any arguments when instantiating
          this class. The default parameters should work out of the box.

          However, if the constructor is unable to automatically identify
          the Arduino device, a port name should be explicitly specified.

          If you specify a baud rate other than the default 115200 baud, you
          must modify the arduino sketch to match the specified baud rate.
        """

        if port is None:
            port = self.__detect_port()

        self.serial = serial.Serial(port, baudrate)
        if not self.serial.isOpen():
            raise serial.SerialException('Arduino device not found.')

        # # used to get mouse position and screen dimensions
        # self.__tk = tkinter.Tk()

        # this flag denoting whether a command is has been completed
        # all module calls are blocking until the Arduino command is complete
        self.__command_complete = threading.Event()

        # read and parse bytes from the serial buffer
        serial_reader = threading.Thread(target=self.__read_buffer)
        serial_reader.daemon = True
        serial_reader.start()

    def open(self, port=None, baudrate=115200):
        """
        Args:
          port (str, optional): Device name or port number number or None.
          baudrate (str, optional): Baud rate such as 9600 or 115200 etc.
        Raises:
          SerialException: In the case the device cannot be found.
        Note:
          You should not have to specify any arguments when instantiating
          this class. The default parameters should work out of the box.

          However, if the constructor is unable to automatically identify
          the Arduino device, a port name should be explicitly specified.

          If you specify a baud rate other than the default 115200 baud, you
          must modify the arduino sketch to match the specified baud rate.
        """

        if port is None:
            port = self.__detect_port()

        self.serial = serial.Serial(port, baudrate)
        if not self.serial.isOpen():
            raise serial.SerialException('Arduino device not found.')

        # # used to get mouse position and screen dimensions
        # self.__tk = tkinter.Tk()

        # this flag denoting whether a command is has been completed
        # all module calls are blocking until the Arduino command is complete
        self.__command_complete = threading.Event()

        # read and parse bytes from the serial buffer
        serial_reader = threading.Thread(target=self.__read_buffer)
        serial_reader.daemon = True
        serial_reader.start()

    def press(self, button=keymouse.MOUSE_LEFT):
        if button in keymouse.MOUSE_BUTTONS:
            self.__write_byte(keymouse.MOUSE_CMD)
            self.__write_byte(keymouse.MOUSE_PRESS)
            self.__write_byte(button)

        elif isinstance(button, int):
            self.__write_byte(keymouse.KEYBOARD_CMD)
            self.__write_byte(keymouse.KEYBOARD_PRESS)
            self.__write_byte(button)

        elif isinstance(button, str) and len(button) == 1:
            self.__write_byte(keymouse.KEYBOARD_CMD)
            self.__write_byte(keymouse.KEYBOARD_PRESS)
            self.__write_byte(ord(button))

        else:
            raise ValueError('Not a valid mouse or keyboard button.')

        self.__command_complete.wait()

    def release(self, button=keymouse.MOUSE_LEFT):
        if button in keymouse.MOUSE_BUTTONS:
            self.__write_byte(keymouse.MOUSE_CMD)
            self.__write_byte(keymouse.MOUSE_RELEASE)
            self.__write_byte(button)

        elif isinstance(button, int):
            self.__write_byte(keymouse.KEYBOARD_CMD)
            self.__write_byte(keymouse.KEYBOARD_RELEASE)
            self.__write_byte(button)

        elif isinstance(button, str) and len(button) == 1:
            self.__write_byte(keymouse.KEYBOARD_CMD)
            self.__write_byte(keymouse.KEYBOARD_RELEASE)
            self.__write_byte(ord(button))

        else:
            raise ValueError('Not a valid mouse or keyboard button.')

        self.__command_complete.wait()

    def release_all(self):
        self.__write_byte(keymouse.KEYBOARD_CMD)
        self.__write_byte(keymouse.KEYBOARD_RELEASE_ALL)

        self.__command_complete.wait()

    def write(self, keys, endl=False):
        if isinstance(keys, int):
            self.__write_byte(keymouse.KEYBOARD_CMD)
            self.__write_byte(keymouse.KEYBOARD_WRITE)
            self.__write_byte(keys)

        elif isinstance(keys, str) and len(keys) == 1:
            self.__write_byte(keymouse.KEYBOARD_CMD)
            self.__write_byte(keymouse.KEYBOARD_WRITE)
            self.__write_byte(ord(keys))

        elif isinstance(keys, str):
            if not endl:
                self.__write_byte(keymouse.KEYBOARD_CMD)
                self.__write_byte(keymouse.KEYBOARD_PRINT)
                self.__write_str(keys)
            else:
                self.__write_byte(keymouse.KEYBOARD_CMD)
                self.__write_byte(keymouse.KEYBOARD_PRINTLN)
                self.__write_str(keys)

        else:
            raise ValueError('Not a valid keyboard keystroke. ' +
                             'Must be type `int` or `char` or `str`.')

        self.__command_complete.wait()

    def type(self, message, wpm=80, mistakes=True, accuracy=96):
        if not isinstance(message, str):
            raise ValueError('Invalid keyboard message. ' +
                             'Must be type `str`.')

        if not isinstance(wpm, int) and wpm < 1 or wpm > 255:
            raise ValueError('Invalid value for `WPM`. ' +
                             'Must be type `int`: 1 <= WPM <= 255.')

        if not isinstance(mistakes, bool):
            raise ValueError('Invalid value for `mistakes`. ' +
                             'Must be type `bool`.')

        if not isinstance(accuracy, int) and accuracy < 1 or accuracy > 100:
            raise ValueError('Invalid value for `accuracy`. ' +
                             'Must be type `int`: 1 <= accuracy <= 100.')

        self.__write_byte(keymouse.KEYBOARD_CMD)
        self.__write_byte(keymouse.KEYBOARD_TYPE)
        self.__write_str(message)
        self.__write_byte(wpm)
        self.__write_byte(mistakes)
        self.__write_byte(accuracy)

        self.__command_complete.wait()

    def click(self, button=keymouse.MOUSE_LEFT):
        if button not in keymouse.MOUSE_BUTTONS:
            raise ValueError('Not a valid mouse button.')

        self.__write_byte(keymouse.MOUSE_CMD)
        self.__write_byte(keymouse.MOUSE_CLICK)
        self.__write_byte(button)

        self.__command_complete.wait()

    def fast_click(self, button):
        if button not in keymouse.MOUSE_BUTTONS:
            raise ValueError('Not a valid mouse button.')

        self.__write_byte(keymouse.MOUSE_CMD)
        self.__write_byte(keymouse.MOUSE_FAST_CLICK)
        self.__write_byte(button)

        self.__command_complete.wait()

    def move(self, dest_x, dest_y):
        if not isinstance(dest_x, (int, float)) and \
                not isinstance(dest_y, (int, float)):
            raise ValueError('Invalid mouse coordinates. ' +
                             'Must be type `int` or `float`.')

        self.__write_byte(keymouse.MOUSE_CMD)
        self.__write_byte(keymouse.MOUSE_MOVE)
        self.__write_short(dest_x)
        self.__write_short(dest_y)

        self.__command_complete.wait()

    def bezier_move(self, dest_x, dest_y):
        if not isinstance(dest_x, (int, float)) and \
                not isinstance(dest_y, (int, float)):
            raise ValueError('Invalid mouse coordinates. ' +
                             'Must be `int` or `float`.')

        self.__write_byte(keymouse.MOUSE_CMD)
        self.__write_byte(keymouse.MOUSE_BEZIER)
        self.__write_short(dest_x)
        self.__write_short(dest_y)

        self.__command_complete.wait()

    def close(self):
        self.serial.close()
        return True

    def __detect_port(self):
        ports = serial.tools.list_ports.comports()
        arduino_port = None

        for port in ports:
            if 'Arduino' in port[1]:
                arduino_port = port[0]

        return arduino_port

    def __read_buffer(self):
        while True:
            byte = ord(self.serial.read())

            if byte == keymouse.MOUSE_CALIBRATE:
                self.__calibrate_mouse()

            elif byte == keymouse.SCREEN_CALIBRATE:
                self.__calibrate_screen()

            elif byte == keymouse.COMMAND_COMPLETE:
                self.__command_complete.set()
                self.__command_complete.clear()

    def __calibrate_screen(self):
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)
        # print(width)
        height = user32.GetSystemMetrics(1)
        # print(height)
        self.__write_short(width)
        self.__write_short(height)

    def __calibrate_mouse(self):
        x, y = win32api.GetCursorPos()
        # XY 현위치
        # print(x , y)

        self.__write_short(x)
        self.__write_short(y)

    def __write_str(self, string):
        for char in string:
            self.__write_byte(ord(char))
        self.__write_byte(0x00)

    def __write_byte(self, byte):
        struct_pack = struct.pack('<B', byte)
        self.serial.write(struct_pack)

    def __write_short(self, short):
        struct_pack = struct.pack('<H', int(short))
        self.serial.write(struct_pack)

# 캡쳐 이미지 클래스
class capture():
    MyPos_templ = cv2.imread('./img/My_Position.png', cv2.IMREAD_COLOR)
    MyPos_templ_mask = cv2.imread('./img/My_Position_mask.png', cv2.IMREAD_COLOR)
    Rune_templ = cv2.imread('./img/Is_Rune.png', cv2.IMREAD_COLOR)
    Rune_templ_mask = cv2.imread('./img/Is_Rune_mask.png', cv2.IMREAD_COLOR)
    Rune_Check_templ = cv2.imread('./img/Rune_Check.png', cv2.IMREAD_COLOR)
    MiniLU = cv2.imread('./img/minimapLU.png', cv2.IMREAD_COLOR)
    MiniRD = cv2.imread('./img/minimapRD.png', cv2.IMREAD_COLOR)

    # 메이플 켜져있나 확인
    def mapleOn(self):
        hwnd = win32gui.FindWindow(None, "MapleStory")
        if hwnd >= 1:
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            result = left + 3, top + 26, left + 3 + 1366, top + 26 + 768, hwnd
        else:
            # left , top , right , bot , hwnd
            result = 0, 0, 0, 0, 0
        return result

    def miniMap(self, img):
        img = img.crop((0, 0, 500, 500))
        res_pos1 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), capture.MiniLU, cv2.TM_CCORR_NORMED)
        con_pos1 = res_pos1.max()
        loc_pos1 = np.where(res_pos1 == con_pos1)

        res_pos2 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), capture.MiniRD, cv2.TM_CCORR_NORMED)
        con_pos2 = res_pos2.max()
        loc_pos2 = np.where(res_pos2 == con_pos2)
        # img.save("./img/tempmini.png")
        if con_pos1 > 0.95 and con_pos2 > 0.95:
            return loc_pos1[1][0] + 1, loc_pos1[0][0] + 1, loc_pos2[1][0] + 12, loc_pos2[0][0] + 11, con_pos1, con_pos2
        else:
            return 0, 0, 0, 0, con_pos1, con_pos2


    def myPosition(self,img):
        try:
            res_mypos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), capture.MyPos_templ, cv2.TM_CCORR_NORMED, mask=capture.MyPos_templ_mask)
            con_mypos = res_mypos[res_mypos <= 1].max()
            loc_mypos = np.where(res_mypos == con_mypos)
            return loc_mypos[1][0], loc_mypos[0][0]
        except:
            return 0, 0

    def runePosition(self,img):
        try:
            res_runepos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), capture.Rune_templ, cv2.TM_CCORR_NORMED, mask=capture.Rune_templ_mask)
            con_runepos = res_runepos[res_runepos < 1].max()
            loc_runepos = np.where(res_runepos == con_runepos)
            return loc_runepos[1][0], loc_runepos[0][0], con_runepos
        except:
            return 0, 0

# 메인 윈도우 클래스
class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.arduino = None
        self.scriptworker = None
        self.captureworker = None
        self.miniMap = None
        self.mapleOn = None
        self.firstMacro = True
        self.isRun = False
        self.setupUi(self)
        # 버튼 매핑
        self.mainBtn1.clicked.connect(self.onStartClicked)  # 시작
        self.mainBtn2.clicked.connect(self.onStopClicked)  # 중지
        self.mainBtn3.clicked.connect(self.onReloadClicked)  # 불러오기
        self.checkBox1.stateChanged.connect(self.chkFunction)  # 무한반복
        self.checkBox2.stateChanged.connect(self.chkFunction)  # 룬체크(딥러닝안함)

    def onStartClicked(self):
        # print("start 버튼")
        self.textInputTB1("시작합니다.")
        self.startMacro()

    def onStopClicked(self):
        # print("stop 버튼")
        try:
            self.captureworker.pause()
        except:
            print("매크로가 실행중이지 않습니다.")
        try:
            self.scriptworker.pause()
        except:
            print("매크로가 실행중이지 않습니다.")
            return
        self.isRun = False
        self.textInputTB1("중지합니다.")

    def onReloadClicked(self):
        # print("load 버튼")
        self.textInputTB1("스크립트를 불러옵니다.")

    def chkFunction(self):
        global rune
        global inficheck
        # 무한반복
        if self.checkBox1.isChecked(): print("무한반복안함"); inficheck = 1
        if not self.checkBox1.isChecked(): print("무한반복함"); inficheck = 0

        # 룬체크
        if self.checkBox2.isChecked(): print("룬체크안함"); rune[3] = 1
        if not self.checkBox2.isChecked(): print("룬체크함"); rune[3] = 0

    # 텍스트 넣어주기 tI
    @pyqtSlot(str)
    def textInputTB1(self, txt):
        # print("텍스트 넣어주기 함수")
        self.mainTB1.append(txt)
        scrollbar = self.mainTB1.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    ### 기본 시작 매크로###
    def startMacro(self):
        global mapleOn
        global miniMap
        if self.isRun: print("이미 실행중입니다."); return
        self.isRun = True
        # 첫 시작눌렀을때 아두이노 세팅
        if self.firstMacro:
            print("아두이노 확인")
            try:
                self.arduino = Arduino()
                print("아두이노 확인 완료")
                self.firstMacro = False
            except:
                print("아두이노 연결이 확인되지 않습니다")
                print("중지합니다.")
                self.isRun = False
                return
        # 두번째 시작을 눌렀을때
        else:
            try:
                print("아두이노 마우스 체크중 마우스 건들 ㄴㄴ")
                self.arduino.move(30, 30)
                print("아두이노 연결 확인 완료")
            except:
                try:
                    self.arduino = Arduino()
                    print("아두이노 재연결 완료")
                    self.firstMacro = False
                except:
                    print("아두이노 연결이 확인되지 않습니다")
                    print("중지합니다.")
                    self.isRun = False
                    return

        print("메이플 프로세스확인")
        mapleOn = capture.mapleOn(self)
        if mapleOn[4] == 0:
            print("메이플 확인 안됨")
            print("중지합니다.")
            self.isRun = False
            return
        print(mapleOn)
        print("메이플 미니맵 확인")
        bbox = (mapleOn[0], mapleOn[1], mapleOn[2], mapleOn[3])
        screen = ImageGrab.grab(bbox)
        # 시작 찰칵찰칵이
        screen.save("./img/temp.png")
        miniMap = capture.miniMap(self,screen)

        print(miniMap)
        if miniMap[3] == 0:
            print("미니맵 인식안됨")
            print("중지합니다.")
            self.isRun = False
            return

        # print("딥러닝체크")
        print("캡쳐 쓰레드 시작")
        self.captureworker = captureWorker()
        self.captureworker.start()
        self.captureworker.textInputTB1.connect(self.textInputTB1)

        print("스크립트 불러오기")
        print("스크립트 쓰레드 시작")
        self.scriptworker = scriptWorker()
        self.scriptworker.start()
        self.scriptworker.textInputTB1.connect(self.textInputTB1)


        # 매크로상태1 = True
        # 매크로시간1 = time()
        # 매크로1()
        #     # screen = ImageGrab.grab(bbox)
        #     # # 내위치 찾기
        #     # crop_img = screen.crop(bboxMini)
        #     # 내위치 = cp.myPosition(crop_img)
        #
        #     # 2초에 한번 위치 입력
        #     if 켜진시간 % 2 == 0:
        #         self.텍스트박스에입력하기(f'내위치 : {내위치}')
        #     # 3초에 한번 룬 확인
        #     if 켜진시간 % 3 == 0:
        #         if not 룬상태:
        #             룬시간 = 0
        #             룬위치 = cp.runePosition(crop_img)
        #             if 룬위치[2] >= 0.98:
        #                 self.텍스트박스에입력하기(f'룬위치 : {룬위치}')
        #                 룬상태 = True
        #                 룬시간 = time()
        #         else:
        #             self.텍스트박스에입력하기(f'룬위치 : {룬위치}')
        #             if time() - 룬시간 > 30:
        #                 print("룬 시간 초과!!")
        #     켜진시간 += 메인주기
        #     켜진시간 = round(켜진시간, 2)
        #     sleep(메인주기)
        # else:
        #     현재상태 = False
        #     매크로상태1 = False
        #     self.isRun = False
        #     print("매크로 종료")


# 캡쳐쓰레드
class captureWorker(QThread):
    textInputTB1 = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.num = 0
        self.running = True

    def run(self):
        global stat
        global mapleOn
        global miniMap
        bbox = (mapleOn[0], mapleOn[1], mapleOn[2], mapleOn[3])
        bboxMini = (miniMap[0],miniMap[1],miniMap[2],miniMap[3])
        while self.running:
            # 스샷
            screen = ImageGrab.grab(bbox)
            # 내위치 찾기
            crop_img = screen.crop(bboxMini)
            stat = capture.myPosition(self,crop_img)
            self.textInputTB1.emit("내위치 " + str(stat[0]) + str(stat[1]))
            self.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False
        print("캡쳐 쓰레드 중지")


# 스크립트 쓰레드
class scriptWorker(QThread):
    textInputTB1 = pyqtSignal(str)
    global stat

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            print("스크립트쓰레드")
            self.textInputTB1.emit("스크립트쓰레드 시작")
            self.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False
        print("스크립트 쓰레드 중지")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()






