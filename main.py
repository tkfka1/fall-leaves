from lib2to3.pgen2 import token
import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import cv2
import numpy as np
import win32gui
import win32api
from PIL import ImageGrab , Image
import serial.tools.list_ports
import serial.tools.list_ports
import threading
import serial
import struct
import ctypes
import sys
import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands
import time
import schedule

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
stat = 0, 0
# 룬 [0,1] 위치 xy [2] 룬 여부 [3] 룬체크 0은 체크함 1은 체크안함
global rune
rune = 0, 0
# 무한반복 0 은 반복함 1은 반복안함
global runecheck
runecheck = 0
global inficheck
inficheck = 0

global ardu
ardu = None
#디스코드 상태
global disstat
disstat = 0
#디스코드 토큰
global distoken
distoken = 'MTAwNjQ5NzUwNjk3ODQ0NzM5MA.GJBqsv.Ix6l_zGHOYhPGl6GsREEQOPiyD8aG3NO30lXP0'

global bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)

global channel
channel = 1006538980956831764
global user
user = 324926800805494784

# APPLICATION ID
# 1006497506978447390
# PUBLIC KEY
# 2ad8a8019dc74bdab341b141b4e31bf60e45bf33326800c31c6a50a1eb6eda1c
# miari-1
# MTAwNjQ5NzUwNjk3ODQ0NzM5MA.GJBqsv.Ix6l_zGHOYhPGl6GsREEQOPiyD8aG3NO30lXP0
# link
# https://discord.com/oauth2/authorize?client_id=1006497506978447390&permissions=8&scope=bot

#### 만들거
## 1. 디코로 시작하기
# 2. 디코로 중지
# 3. 시작후 움직여서 사냥터 가기
# 4.
# user = client.get_user(381870129706958858)
# await user.send('👀')
# channel = client.get_channel(12324234183172)
# await channel.send('hello')


@bot.event
async def on_ready():
    print('Bot Is Ready')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("재밌는 일"))
    await bt()


# 받으면 삭제하고 바꾸기
@bot.event
async def on_message(message):
    message_content = message.content
    bad = message_content.find("pong")
    print(bad)
    if bad >= 0:
        await message.channel.send("읏우")
        await message.delete()
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    file = discord.File("temp.png")
    embed = discord.Embed(title='알림', description='거탐', color=0xFF5733)
    embed.set_image(url="attachment://temp.png")
    await ctx.send(embed=embed, file=file)



#disstat = 0  실행중 1 정상동작중 2 룬찾기 3 알람 4 거탐 5 비올레타
# 디스코드 모니터 쓰레드
async def bt():
    global channel
    global user
    channel = bot.get_channel(channel)
    user = await bot.fetch_user(user)

    await bot.wait_until_ready()
    i = 0
    while not bot.is_closed():
        # await channel.send("읏우")
        # await user.send('우누누우')
        # print("웃우")
        if disstat == 0:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game("실행중"))
        elif disstat == 1:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game("정상동작중"))
            if i == 600:
                i = 0
                await channel.send("정상동작중입니다.")
            i = i+1
        elif disstat == 2:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game("룬찾기"))
        elif disstat == 3:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game("알람"))
            await user.send('(」・ω・)」우―！(／・ω・)／냐―！')
        elif disstat == 4:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game("거탐"))
            await user.send('(＼(・ω ・＼)SAN치！(／・ω・)／FIN치！')
        elif disstat == 5:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game("비올레타"))
        await asyncio.sleep(1)



# 키마 세팅 클래스
class Keymouse():
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
            raise serial.SerialException("Arduino device not found.")

        # this flag denoting whether a command is has been completed
        # all module calls are blocking until the Arduino command is complete
        self.__command_complete = threading.Event()

        # read and parse bytes from the serial buffer
        serial_reader = threading.Thread(target=self.__read_buffer)
        serial_reader.daemon = True
        serial_reader.start()

    def press(self, button=Keymouse.MOUSE_LEFT):
        if button in Keymouse.MOUSE_BUTTONS:
            self.__write_byte(Keymouse.MOUSE_CMD)
            self.__write_byte(Keymouse.MOUSE_PRESS)
            self.__write_byte(button)

        elif isinstance(button, int):
            self.__write_byte(Keymouse.KEYBOARD_CMD)
            self.__write_byte(Keymouse.KEYBOARD_PRESS)
            self.__write_byte(button)

        elif isinstance(button, str) and len(button) == 1:
            self.__write_byte(Keymouse.KEYBOARD_CMD)
            self.__write_byte(Keymouse.KEYBOARD_PRESS)
            self.__write_byte(ord(button))

        else:
            raise ValueError("Not a valid mouse or keyboard button.")

        self.__command_complete.wait()

    def release(self, button=Keymouse.MOUSE_LEFT):
        if button in Keymouse.MOUSE_BUTTONS:
            self.__write_byte(Keymouse.MOUSE_CMD)
            self.__write_byte(Keymouse.MOUSE_RELEASE)
            self.__write_byte(button)

        elif isinstance(button, int):
            self.__write_byte(Keymouse.KEYBOARD_CMD)
            self.__write_byte(Keymouse.KEYBOARD_RELEASE)
            self.__write_byte(button)

        elif isinstance(button, str) and len(button) == 1:
            self.__write_byte(Keymouse.KEYBOARD_CMD)
            self.__write_byte(Keymouse.KEYBOARD_RELEASE)
            self.__write_byte(ord(button))

        else:
            raise ValueError("Not a valid mouse or keyboard button.")

        self.__command_complete.wait()

    def release_all(self):
        self.__write_byte(Keymouse.KEYBOARD_CMD)
        self.__write_byte(Keymouse.KEYBOARD_RELEASE_ALL)

        self.__command_complete.wait()

    def write(self, keys, endl=False):
        if isinstance(keys, int):
            self.__write_byte(Keymouse.KEYBOARD_CMD)
            self.__write_byte(Keymouse.KEYBOARD_WRITE)
            self.__write_byte(keys)

        elif isinstance(keys, str) and len(keys) == 1:
            self.__write_byte(Keymouse.KEYBOARD_CMD)
            self.__write_byte(Keymouse.KEYBOARD_WRITE)
            self.__write_byte(ord(keys))

        elif isinstance(keys, str):
            if not endl:
                self.__write_byte(Keymouse.KEYBOARD_CMD)
                self.__write_byte(Keymouse.KEYBOARD_PRINT)
                self.__write_str(keys)
            else:
                self.__write_byte(Keymouse.KEYBOARD_CMD)
                self.__write_byte(Keymouse.KEYBOARD_PRINTLN)
                self.__write_str(keys)

        else:
            raise ValueError(
                "Not a valid keyboard keystroke. "
                + "Must be type `int` or `char` or `str`."
            )

        self.__command_complete.wait()

    def type(self, message, wpm=80, mistakes=True, accuracy=96):
        if not isinstance(message, str):
            raise ValueError("Invalid keyboard message. " + "Must be type `str`.")

        if not isinstance(wpm, int) and wpm < 1 or wpm > 255:
            raise ValueError(
                "Invalid value for `WPM`. " + "Must be type `int`: 1 <= WPM <= 255."
            )

        if not isinstance(mistakes, bool):
            raise ValueError("Invalid value for `mistakes`. " + "Must be type `bool`.")

        if not isinstance(accuracy, int) and accuracy < 1 or accuracy > 100:
            raise ValueError(
                "Invalid value for `accuracy`. "
                + "Must be type `int`: 1 <= accuracy <= 100."
            )

        self.__write_byte(Keymouse.KEYBOARD_CMD)
        self.__write_byte(Keymouse.KEYBOARD_TYPE)
        self.__write_str(message)
        self.__write_byte(wpm)
        self.__write_byte(mistakes)
        self.__write_byte(accuracy)

        self.__command_complete.wait()

    def click(self, button=Keymouse.MOUSE_LEFT):
        if button not in Keymouse.MOUSE_BUTTONS:
            raise ValueError("Not a valid mouse button.")

        self.__write_byte(Keymouse.MOUSE_CMD)
        self.__write_byte(Keymouse.MOUSE_CLICK)
        self.__write_byte(button)

        self.__command_complete.wait()

    def fast_click(self, button):
        if button not in Keymouse.MOUSE_BUTTONS:
            raise ValueError("Not a valid mouse button.")

        self.__write_byte(Keymouse.MOUSE_CMD)
        self.__write_byte(Keymouse.MOUSE_FAST_CLICK)
        self.__write_byte(button)

        self.__command_complete.wait()

    def move(self, dest_x, dest_y):
        if not isinstance(dest_x, (int, float)) and not isinstance(
            dest_y, (int, float)
        ):
            raise ValueError(
                "Invalid mouse coordinates. " + "Must be type `int` or `float`."
            )

        self.__write_byte(Keymouse.MOUSE_CMD)
        self.__write_byte(Keymouse.MOUSE_MOVE)
        self.__write_short(dest_x)
        self.__write_short(dest_y)

        self.__command_complete.wait()

    def bezier_move(self, dest_x, dest_y):
        if not isinstance(dest_x, (int, float)) and not isinstance(
            dest_y, (int, float)
        ):
            raise ValueError(
                "Invalid mouse coordinates. " + "Must be `int` or `float`."
            )

        self.__write_byte(Keymouse.MOUSE_CMD)
        self.__write_byte(Keymouse.MOUSE_BEZIER)
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
            if "Arduino" in port[1]:
                arduino_port = port[0]

        return arduino_port

    def __read_buffer(self):
        while True:
            byte = ord(self.serial.read())

            if byte == Keymouse.MOUSE_CALIBRATE:
                self.__calibrate_mouse()

            elif byte == Keymouse.SCREEN_CALIBRATE:
                self.__calibrate_screen()

            elif byte == Keymouse.COMMAND_COMPLETE:
                self.__command_complete.set()
                self.__command_complete.clear()

    def __calibrate_screen(self):
        width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        self.__write_short(width)
        self.__write_short(height)

    def __calibrate_mouse(self):
        x, y = win32api.GetCursorPos()

        self.__write_short(x)
        self.__write_short(y)

    def __write_str(self, string):
        for char in string:
            self.__write_byte(ord(char))
        self.__write_byte(0x00)

    def __write_byte(self, byte):
        struct_pack = struct.pack("<B", byte)
        self.serial.write(struct_pack)

    def __write_short(self, short):
        struct_pack = struct.pack("<H", int(short))
        self.serial.write(struct_pack)


# 캡쳐 이미지 클래스
class Capture:
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
        res_pos1 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.MiniLU, cv2.TM_CCORR_NORMED)
        con_pos1 = res_pos1.max()
        loc_pos1 = np.where(res_pos1 == con_pos1)

        res_pos2 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.MiniRD, cv2.TM_CCORR_NORMED)
        con_pos2 = res_pos2.max()
        loc_pos2 = np.where(res_pos2 == con_pos2)
        # img.save("./img/tempmini.png")
        if con_pos1 > 0.95 and con_pos2 > 0.95:
            return loc_pos1[1][0] + 1, loc_pos1[0][0] + 1, loc_pos2[1][0] + 12, loc_pos2[0][0] + 11, con_pos1, con_pos2
        else:
            return 0, 0, 0, 0, con_pos1, con_pos2


    def myPosition(self, img):
        try:
            res_mypos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.MyPos_templ, cv2.TM_CCORR_NORMED, mask=Capture.MyPos_templ_mask)
            con_mypos = res_mypos[res_mypos <= 1].max()
            loc_mypos = np.where(res_mypos == con_mypos)
            return loc_mypos[1][0], loc_mypos[0][0]
        except:
            return 0, 0

    def runePosition(self, img):
        try:
            res_runepos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.Rune_templ, cv2.TM_CCORR_NORMED, mask=Capture.Rune_templ_mask)
            con_runepos = res_runepos[res_runepos < 1].max()
            loc_runepos = np.where(res_runepos == con_runepos)
            if con_runepos > 0.98:
                return loc_runepos[1][0], loc_runepos[0][0]
            else:
                return 0, 0
        except:
            return 0, 0

# 메인 윈도우 클래스
class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.arduino = None
        self.scriptworker = None
        self.captureworker = None
        self.discordworker = None
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
        try:
            self.discordworker.pause()
        except:
            print("매크로가 실행중이지 않습니다.")
            return
        self.isRun = False
        self.textInputTB1("중지합니다.")

    def onReloadClicked(self):
        global disstat
        # print("load 버튼")
        self.textInputTB1("스크립트를 불러옵니다.")
        disstat = 3

    def chkFunction(self):
        global runecheck
        global inficheck
        # 무한반복
        if self.checkBox1.isChecked(): print("무한반복안함"); inficheck = 1
        if not self.checkBox1.isChecked(): print("무한반복함"); inficheck = 0

        # 룬체크
        if self.checkBox2.isChecked(): print("룬체크안함"); runecheck = 1
        if not self.checkBox2.isChecked(): print("룬체크함"); runecheck = 0

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
        global ardu
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
                print("아두이노 마우스 체크중 건들 ㄴㄴ")
                self.arduino.release_all()
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
        ardu = self.arduino

        print("메이플 프로세스확인")
        mapleOn = Capture.mapleOn(self)
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
        miniMap = Capture.miniMap(self, screen)

        print(miniMap)
        if miniMap[3] == 0:
            print("미니맵 인식안됨")
            print("중지합니다.")
            self.isRun = False
            return



        # print("딥러닝체크")
        print("캡쳐 쓰레드 시작")
        self.captureworker = CaptureWorker()
        self.captureworker.start()
        self.captureworker.textInputTB1.connect(self.textInputTB1)

        print("스크립트 불러오기")
        print("스크립트 쓰레드 시작")
        self.scriptworker = ScriptWorker()
        self.scriptworker.start()
        self.scriptworker.textInputTB1.connect(self.textInputTB1)

        self.discordworker = DiscordWorker()
        self.discordworker.start()
        #self.discordworker.textInputTB1.connect(self.textInputTB1)


# 캡쳐쓰레드
class CaptureWorker(QThread):
    textInputTB1 = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.capturei = 0
        self.running = True

    def run(self):
        global mapleOn
        global miniMap
        global disstat
        self.bbox = (mapleOn[0], mapleOn[1], mapleOn[2], mapleOn[3])
        self.bboxMini = (miniMap[0], miniMap[1], miniMap[2], miniMap[3])
        disstat = 1
        def myloce():
            global stat
            global rune
            global disstat
            screen = ImageGrab.grab(self.bbox)
            # 내위치 찾기
            crop_img = screen.crop(self.bboxMini)
            stat = Capture.myPosition(self, crop_img)
            if self.capturei == 30:
                self.capturei = 0
                self.textInputTB1.emit("내위치 " + str(stat[0]) + str(stat[1]))
                if runecheck == 0:
                    rune = Capture.runePosition(self, crop_img)
                    if not rune[1] == 0:
                        disstat = 2
                        self.textInputTB1.emit("룬위치 " + str(rune[0]) + str(rune[1]))
            self.capturei += 1
        # job1 내위치 0.1초마다
        job1 = schedule.every(0.1).seconds.do(myloce)
        while self.running:
            schedule.run_pending()
            time.sleep(0.1)
        else:
            schedule.cancel_job(job1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False
        print("캡쳐 쓰레드 중지")


# 스크립트 쓰레드
class ScriptWorker(QThread):
    textInputTB1 = pyqtSignal(str)
    global stat
    global rune

    def __init__(self):
        super().__init__()
        self.runestack = None
        self.starttime = None
        self.scripti = None
        self.running = True

    def 빠른이동(self):
        print("빠른이동")
    def 일반이동(self):
        print("일반이동")

    def run(self):
        self.scripti = 0
        self.runeloce = 0, 0
        self.runestack = 0
        global disstat
        global ardu
        while self.running:
            #만약 룬
            #if 룬
            if disstat == 2:
                if not rune[1] == 0:
                    self.starttime = time.time()
                    self.runeloce = rune
                차이x = stat[0] - self.runeloce[0]
                차이y = stat[1] - self.runeloce[1]
                if 차이x > 40:
                    print("왼쪽으로많이 이동")
                    ardu.release(Keymouse.RIGHT_ARROW)
                    ardu.press(Keymouse.LEFT_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.3)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.2)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    time.sleep(1)
                elif 40 > 차이x > 6:
                    print("왼쪽 이동")
                    ardu.release(Keymouse.RIGHT_ARROW)
                    ardu.press(Keymouse.LEFT_ARROW)
                    time.sleep(0.3)
                elif 7 > 차이x > 1:
                    print("왼쪽 조금 이동")
                    ardu.release(Keymouse.RIGHT_ARROW)
                    ardu.press(Keymouse.LEFT_ARROW)
                elif -40 > 차이x:
                    print("오른쪽으로많이 이동")
                    ardu.release(Keymouse.LEFT_ARROW)
                    ardu.press(Keymouse.RIGHT_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.3)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.2)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    time.sleep(1)
                    time.sleep(1)
                elif -7 > 차이x > -40:
                    print("오른쪽 이동")
                    ardu.release(Keymouse.LEFT_ARROW)
                    ardu.press(Keymouse.RIGHT_ARROW)
                    time.sleep(0.3)
                elif -1 > 차이x > -7:
                    print("오른쪽 조금 이동")
                    ardu.release(Keymouse.LEFT_ARROW)
                    ardu.press(Keymouse.RIGHT_ARROW)
                if 차이y > 40:
                    print("위쪽으로많이 이동")
                    ardu.press(Keymouse.UP_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.UP_ARROW)
                elif 40 > 차이y > 6:
                    print("위쪽 이동")
                    ardu.press(Keymouse.UP_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.UP_ARROW)
                elif 7 > 차이y > 1:
                    print("위쪽 조금 이동")
                    ardu.press(Keymouse.UP_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.UP_ARROW)
                elif -40 > 차이y:
                    print("아래쪽으로많이 이동")
                    ardu.press(Keymouse.DOWN_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.4)
                    ardu.release(Keymouse.DOWN_ARROW)
                elif -7 > 차이y > -40:
                    print("아래쪽 이동")
                    ardu.release_all()
                    ardu.press(Keymouse.DOWN_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.4)
                    ardu.release(Keymouse.DOWN_ARROW)
                elif -1 > 차이y > -7:
                    print("아래쪽 조금 이동")
                    ardu.release_all()
                    ardu.press(Keymouse.DOWN_ARROW)
                    time.sleep(0.1)
                    ardu.press(Keymouse.LEFT_ALT)
                    time.sleep(0.1)
                    ardu.release(Keymouse.LEFT_ALT)
                    time.sleep(0.4)
                    ardu.release(Keymouse.DOWN_ARROW)
                if 0 <= abs(stat[0] - self.runeloce[0]) < 2 and 0 <= abs(stat[1] - self.runeloce[1]) < 2:
                    ardu.release_all()
                    self.runestack += 1
                    if self.runestack == 10:
                        self.runestack = 0
                        print("룬 해제")
                        ardu.press(" ")
                        time.sleep(0.2)
                        ardu.release(" ")
                        disstat = 1
                        print(time.time()-self.starttime)
                time.sleep(0.1)
            else:
                #내위치
                print("내위치")
                print(stat)
                time.sleep(0.1)






    def resume(self):
        self.running = True

    def pause(self):
        self.running = False
        print("스크립트 쓰레드 중지")


# 디스코드 쓰레드
class DiscordWorker(QThread):
    global distoken
    global bot

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        bot.run(distoken)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False
        print("디스코드 쓰레드 중지")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()






