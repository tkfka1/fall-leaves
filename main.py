import distutils
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
import win32gui
import win32api
from PIL import ImageGrab, Image
import serial.tools.list_ports
import threading
import serial
import struct
import sys
import asyncio
import discord
from discord.ext import commands
import time
import schedule
import tensorflow as tf
import configparser

form_class = uic.loadUiType("mainWindow.ui")[0]
global mytype
global caplil
global maplecheck
global minimapcheck
global loccheck
global runecheck
global runedeep
global ldcheck
global useardu
global usedisbot
global distoken
global channel
global user
mytype = "기본동작모드"
caplil = 0.1
maplecheck = False
minimapcheck = False
loccheck = False
runecheck = False
runedeep = False
ldcheck = False
useardu = False
usedisbot = False
distoken = ""
channel = 0
user = 0

# config 만들기
def make_config():
    global mytype
    global caplil
    global loccheck
    global runecheck
    global runedeep
    global ldcheck
    global useardu
    global usedisbot
    global distoken
    global channel
    global user
    config = configparser.ConfigParser()
    # 설정파일 오브젝트 만들기
    config['main'] = {}
    config['main']['시작타입'] = mytype
    config['capture'] = {}
    config['capture']['캡쳐 주기'] = str(caplil)
    config['capture']['메이플체크'] = str(maplecheck)
    config['capture']['미니맵체크'] = str(minimapcheck)
    config['capture']['위치체크'] = str(loccheck)
    config['capture']['룬체크'] = str(runecheck)
    config['capture']['룬딥러닝'] = str(runedeep)
    config['capture']['거탐체크'] = str(ldcheck)
    config['script'] = {}
    config['script']['아두이노 사용'] = str(useardu)
    config['discord'] = {}
    config['discord']['봇 사용'] = str(usedisbot)
    config['discord']['디스코드 토큰'] = distoken
    config['discord']['디스코드 채널'] = str(channel)
    config['discord']['디스코드 유저'] = str(user)
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

# config 없다면
if not os.path.isfile("config.ini"):
    make_config()

# config and 변수 ini
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

cf_main_type = config['main']['시작타입']
mytype = cf_main_type

cf_capture_lil = config['capture']['캡쳐 주기']
caplil = round(float(cf_capture_lil), 2)

cf_capture_maplecheck = config['capture']['메이플체크']
maplecheck = distutils.util.strtobool(cf_capture_maplecheck)

cf_capture_minimapcheck = config['capture']['미니맵체크']
minimapcheck = distutils.util.strtobool(cf_capture_minimapcheck)

cf_capture_loc = config['capture']['위치체크']
loccheck = distutils.util.strtobool(cf_capture_loc)

cf_capture_rune = config['capture']['룬체크']
runecheck = distutils.util.strtobool(cf_capture_rune)

cf_capture_runedeep = config['capture']['룬딥러닝']
runedeep = distutils.util.strtobool(cf_capture_runedeep)

cf_capture_ld = config['capture']['거탐체크']
ldcheck = distutils.util.strtobool(cf_capture_ld)

cf_script_ardu = config['script']['아두이노 사용']
useardu = distutils.util.strtobool(cf_script_ardu)

cf_discord_bot = config['discord']['봇 사용']
usedisbot = distutils.util.strtobool(cf_discord_bot)

cf_discord_tokken = config['discord']['디스코드 토큰']
distoken = cf_discord_tokken

cf_discord_channel = config['discord']['디스코드 채널']
channel = int(cf_discord_channel)

cf_discord_user = config['discord']['디스코드 유저']
user = int(cf_discord_user)

global ardu
ardu = None

global PATH_TO_MODELS
PATH_TO_MODELS = './RuneAuto/saved_model'
global model
model = None

global screen
screen = Image.open("./img/rune_ready.jpg")

# 메이플 x, y , w , h , hwnd
global mapleOn
mapleOn = 0, 0, 0, 0, 0

# 미니맵 x, y , w, h ,적중률 왼위 오른아래
global miniMap
miniMap = 0, 0, 0, 0, 0, 0

# [0] 내위치 X [1] 내위치 Y
global stat
stat = 0, 0
# 룬 [0,1] 위치 xy [2] 룬 여부 [3] 룬체크 0은 체크함 1은 체크안함
global rune
rune = 0, 0
global runetime
runetime = 0

global sc
sc = None
# 디스코드 상태
global disstat
disstat = 0

global bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)


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


# disstat = 0  중지 1 정상동작중 2 룬찾기 3 알람 4 거탐 5 비올레타
# 디스코드 모니터
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
            await bot.change_presence(status=discord.Status.online, activity=discord.Game("중지"))
        elif disstat == 1:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game("정상동작"))
            if i == 600:
                i = 0
                await channel.send("정상동작중입니다.")
            i = i + 1
        elif disstat == 2:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game("일시정지"))
        elif disstat == 3:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game("룬찾기"))
        elif disstat == 4:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game("거탐"))
            await user.send('(＼(・ω ・＼)SAN치！(／・ω・)／FIN치！')
        elif disstat == 5:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game("비올레타"))
            await user.send('(」・ω・)」우―！(／・ω・)／냐―！')

        await asyncio.sleep(1)

# 키마 세팅 클래스
class Keymouse():
    # Mouse basic commands and arguments
    MOUSE_CMD = 0xE0
    MOUSE_CALIBRATE = 0xE1
    MOUSE_PRESS = 0xE2
    MOUSE_RELEASE = 0xE3

    MOUSE_CLICK = 0xE4
    MOUSE_FAST_CLICK = 0xE5
    MOUSE_MOVE = 0xE6
    MOUSE_BEZIER = 0xE7

    # Mouse buttons
    MOUSE_LEFT = 0xEA
    MOUSE_RIGHT = 0xEB
    MOUSE_MIDDLE = 0xEC
    MOUSE_BUTTONS = [MOUSE_LEFT,
                     MOUSE_MIDDLE,
                     MOUSE_RIGHT]

    # Keyboard commands and arguments
    KEYBOARD_CMD = 0xF0
    KEYBOARD_PRESS = 0xF1
    KEYBOARD_RELEASE = 0xF2
    KEYBOARD_RELEASE_ALL = 0xF3
    KEYBOARD_PRINT = 0xF4
    KEYBOARD_PRINTLN = 0xF5
    KEYBOARD_WRITE = 0xF6
    KEYBOARD_TYPE = 0xF7

    # Arduino keyboard modifiers
    # http://arduino.cc/en/Reference/KeyboardModifiers
    LEFT_CTRL = 0x80
    LEFT_SHIFT = 0x81
    LEFT_ALT = 0x82
    LEFT_GUI = 0x83
    RIGHT_CTRL = 0x84
    RIGHT_SHIFT = 0x85
    RIGHT_ALT = 0x86
    RIGHT_GUI = 0x87
    UP_ARROW = 0xDA
    DOWN_ARROW = 0xD9
    LEFT_ARROW = 0xD8
    RIGHT_ARROW = 0xD7
    BACKSPACE = 0xB2
    TAB = 0xB3
    RETURN = 0xB0
    ESC = 0xB1
    INSERT = 0xD1
    DELETE = 0xD4
    PAGE_UP = 0xD3
    PAGE_DOWN = 0xD6
    HOME = 0xD2
    END = 0xD5
    CAPS_LOCK = 0xC1
    F1 = 0xC2
    F2 = 0xC3
    F3 = 0xC4
    F4 = 0xC5
    F5 = 0xC6
    F6 = 0xC7
    F7 = 0xC8
    F8 = 0xC9
    F9 = 0xCA
    F10 = 0xCB
    F11 = 0xCC
    F12 = 0xCD

    # etc.
    SCREEN_CALIBRATE = 0xFF
    COMMAND_COMPLETE = 0xFE


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
    MiniLU_mask = cv2.imread('./img/minimapLU_mask.png', cv2.IMREAD_COLOR)
    MiniRD_mask = cv2.imread('./img/minimapRD_mask.png', cv2.IMREAD_COLOR)

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
        img = img.crop((0, 0, 400, 400))
        res_pos1 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.MiniLU,
                                     cv2.TM_CCORR_NORMED, mask=Capture.MiniLU_mask)
        con_pos1 = res_pos1.max()
        loc_pos1 = np.where(res_pos1 == con_pos1)

        res_pos2 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.MiniRD,
                                     cv2.TM_CCORR_NORMED, mask=Capture.MiniRD_mask)
        con_pos2 = res_pos2.max()
        loc_pos2 = np.where(res_pos2 == con_pos2)
        # img.save("./img/tempmini.png")
        if con_pos1 > 0.99 and con_pos2 > 0.99:
            return loc_pos1[1][0] + 1, loc_pos1[0][0] + 1, loc_pos2[1][0] + 12, loc_pos2[0][0] + 11, con_pos1, con_pos2
        else:
            return 0, 0, 0, 0, con_pos1, con_pos2

    def myPosition(self, img):
        try:
            res_mypos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.MyPos_templ,
                                          cv2.TM_SQDIFF_NORMED, mask=Capture.MyPos_templ_mask)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res_mypos)
            con_runepos = minVal
            loc_runepos = minLoc
            if con_runepos < 0.01:
                return loc_runepos[0], loc_runepos[1]
            else:
                return 0, 0
        except:
            return 0, 0

    def runePosition(self, img):
        try:
            res_runepos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Capture.Rune_templ,
                                            cv2.TM_SQDIFF_NORMED, mask=Capture.Rune_templ_mask)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res_runepos)
            con_runepos = minVal
            loc_runepos = minLoc
            # img.save("./img/tempmini.png")
            # print(minVal, maxVal, minLoc, maxLoc)
            if con_runepos < 0.01:
                return loc_runepos[0], loc_runepos[1]
            else:
                return 0, 0
        except:
            return 0, 0


## 룬딥쁘러닝
def inference_from_model(image, threshold=None):
    global model
    img = image.copy()
    input_tensor = tf.convert_to_tensor(img)
    input_tensor = input_tensor[tf.newaxis,...]
    model_fn = model.signatures['serving_default']
    output_dict = model_fn(input_tensor)
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key:value[0, :num_detections].numpy()
                    for key,value in output_dict.items()}
    output_dict['num_detections'] = num_detections
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
    if threshold is not None:
        detect_class = np.array([value for index, value in enumerate(output_dict['detection_classes'])
                                    if output_dict['detection_scores'][index] > threshold])
        detect_coord = np.array([value for index, value in enumerate(output_dict['detection_boxes'])
                                 if output_dict['detection_scores'][index] > threshold])

        if len(detect_class) == 0:
            return np.array([0])
        else:
            if len(detect_class) == 1:
                if detect_class[0] == 5:
                    ldx = detect_coord[0, 1] * 1366 + detect_coord[0, 3] * 1366
                    ldy = detect_coord[0, 0] * 768 + detect_coord[0, 2] * 768
                    ldroc = list(map(lambda x: int(x / 2), [ldx, ldy]))
                    return detect_class[0], ldroc
                else:
                    return np.array([0])
            elif len(detect_class) == 2:
                if detect_class[1] == 6:
                    ldx = detect_coord[1, 1] * 1366 + detect_coord[1, 3] * 1366
                    ldy = detect_coord[1, 0] * 768 + detect_coord[1, 2] * 768
                    ldroc = list(map(lambda x: int(x / 2), [ldx, ldy]))
                    return detect_class[1], ldroc
                else:
                    return np.array([0])
            elif len(detect_class) == 4:
                return detect_class
            else:
                return np.array([0])
    else:
        detect_class = output_dict['detection_classes'][:4]
        detect_coord = output_dict['detection_boxes'][:4]
        return detect_class[np.argsort(detect_coord[:, 1])]

# 메인 윈도우 클래스
class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.scriptworker = None
        self.captureworker = None
        self.discordworker = None
        self.firstMacro = True
        self.isRun = False
        self.setupUi(self)
        # 설정 매핑
        if maplecheck:
            self.checkBoxMaple.toggle()
        if minimapcheck:
            self.checkBoxMinimap.toggle()
        if loccheck:
            self.checkBoxLoc.toggle()
        if runecheck:
            self.checkBoxRune.toggle()
        if runedeep:
            self.checkBoxRunedeep.toggle()
        if ldcheck:
            self.checkBoxLd.toggle()
        if useardu:
            self.checkBoxArdu.toggle()
        if usedisbot:
            self.checkBoxBot.toggle()

        # 버튼 매핑
        self.mainBtn1.clicked.connect(self.onStartClicked)  # 시작
        self.mainBtn2.clicked.connect(self.onStopClicked)  # 중지
        self.mainBtn3.clicked.connect(self.onReloadClicked)  # 불러오기
        self.settingBtn.clicked.connect(self.onSettingClicked)  # 룬찾기
        self.mainBtn4.clicked.connect(self.onRuneClicked)  # 룬찾기
        self.testBtn1.clicked.connect(self.onTest1Clicked)  # test1
        self.testBtn2.clicked.connect(self.onTest2Clicked)  # test2
        self.testBtn3.clicked.connect(self.onTest3Clicked)  # test3
        self.checkBoxLoc.stateChanged.connect(self.chkFunction)  # 위치체크
        self.checkBoxRune.stateChanged.connect(self.chkFunction)  # 룬체크
        self.checkBoxRunedeep.stateChanged.connect(self.chkFunction) # 룬딥러닝
        self.checkBoxLd.stateChanged.connect(self.chkFunction) # 거탐체크
        self.checkBoxArdu.stateChanged.connect(self.chkFunction) # 아두이노체크
        self.checkBoxBot.stateChanged.connect(self.chkFunction)  # 디코봇체크
        self.doubleSpinBoxLil.valueChanged.connect(self.lil_changed) # 캡쳐주기 변경
        self.discordTokken.setText(str(distoken))
        self.discordTokken.textChanged.connect(self.tokken_changed)
        self.discordChannel.setText(str(channel))
        self.discordChannel.textChanged.connect(self.channel_changed)
        self.discordUser.setText(str(user))
        self.discordUser.textChanged.connect(self.user_changed)



        # 콤보박스
        self.comboBox.addItem("기본동작모드")
        self.comboBox.addItem("스크립트제작")
        self.comboBox.addItem("test1")
        self.comboBox.addItem("test2")
        self.comboBox.addItem("test3")
        self.comboBox.addItem("test4")
        # 콤보박스 기본 선택
        for v in range(1, self.comboBox.count()):
            if self.comboBox.itemText(v) == mytype:
                self.comboBox.setCurrentIndex(v)
        self.comboBox.currentIndexChanged.connect(self.comboBoxFunction)  # 콤보박스 펑션




    def onStartClicked(self):
        global disstat
        if disstat == 0 or disstat == 2:
            disstat = 1
            self.label_status.setText("정상동작중")
            self.label_status.setStyleSheet(
                "color: #41E881; border-style: solid; border-width: 2px; border-color: #67E841; border-radius: 10px; ")
        self.startMacro()

    def onStopClicked(self):
        global disstat
        # print("stop 버튼")
        self.textInputTB1("중지합니다.")
        try:
            self.captureworker.pause()
        except:
            self.textInputTB1("캡쳐 쓰레드가 실행중이지 않습니다.")
        try:
            self.scriptworker.pause()
        except:
            self.textInputTB1("스크립트 쓰레드가 실행중이지 않습니다.")
        try:
            self.discordworker.pause()
        except:
            self.textInputTB1("디스코드 쓰레드가 실행중이지 않습니다.")
            # return
        self.isRun = False
        disstat = 2
        self.label_status.setText("일시정지")
        self.label_status.setStyleSheet(
            "color: #FF5733; border-style: solid; border-width: 2px; border-color: #FFC300; border-radius: 10px; ")


    def onReloadClicked(self):
        global disstat
        global sc
        # print("load 버튼")
        self.textInputTB1("스크립트를 불러옵니다.")

        filename = QFileDialog.getOpenFileName(directory="./script", filter="script (*.py)")
        filename = filename[0]
        print("open file:", filename)
        if not filename:
            return
        with open(filename):
            print("filename")
            self.textInputTB1(f'{filename}')
            exec(open(f'{filename}', encoding='utf-8').read(), globals())
            sc = filename.split('/')[-1].split('.')[0]
            self.helo = hello()

        self.textInputTB1(f'{sc} script load.')
        self.textInputTB1(f'{self.helo}')

    def onSettingClicked(self):
        make_config()
        QMessageBox.about(self, '저장완료', '세팅이 성공적으로 저장되었습니다.')

    def onRuneClicked(self):
        global mapleOn
        global screen
        global model
        image_array = np.array(screen)
        if model == None:
            self.textInputTB1("딥러닝 모델 불러오는 중.")
            model = tf.saved_model.load(PATH_TO_MODELS)
            with tf.device('/gpu:0'):
                results = inference_from_model(image_array)
            rune_screen = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'./img/rune/{int(time.time())}.jpg', rune_screen)
            self.textInputTB1(str(results))
        else:
            with tf.device('/gpu:0'):
                results = inference_from_model(image_array)
            rune_screen = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'./img/rune/{int(time.time())}.jpg', rune_screen)
            self.textInputTB1(str(results))

    def onTest1Clicked(self):
        print("test1 시작")
        self.time = time.time()
        global ardu
        ardu = Arduino()
        time.sleep(1)
        print(f"test1 종료 걸린시간 = {time.time() - self.time}")

    def onTest2Clicked(self):
        global ardu
        print("test2 시작")
        self.time = time.time()
        gotohunt(self.time)
        print(f"test2 종료 걸린시간 = {time.time() - self.time}")

    def onTest3Clicked(self):
        self.progressBar.setValue(100)

    def chkFunction(self):
        global maplecheck
        global minimapcheck
        global loccheck
        global runecheck
        global runedeep
        global ldcheck
        global useardu
        global usedisbot
        # 메이플체크
        if self.checkBoxMaple.isChecked(): maplecheck = True
        if not self.checkBoxMaple.isChecked(): maplecheck = False
        # 미니맵체크
        if self.checkBoxMinimap.isChecked(): minimapcheck = True
        if not self.checkBoxMinimap.isChecked(): minimapcheck = False
        # 위치체크
        if self.checkBoxLoc.isChecked(): loccheck = True
        if not self.checkBoxLoc.isChecked(): loccheck = False
        # 룬체크
        if self.checkBoxRune.isChecked(): runecheck = True
        if not self.checkBoxRune.isChecked(): runecheck = False
        # 룬딥러닝체크
        if self.checkBoxRunedeep.isChecked(): runedeep = True
        if not self.checkBoxRunedeep.isChecked(): runedeep = False
        # 거탐체크
        if self.checkBoxRune.isChecked(): ldcheck = True
        if not self.checkBoxRune.isChecked(): ldcheck = False
        # 아두이노 체크
        if self.checkBoxArdu.isChecked(): useardu = True
        if not self.checkBoxArdu.isChecked(): useardu = False
        # 디코봇체크
        if self.checkBoxBot.isChecked(): usedisbot = True
        if not self.checkBoxBot.isChecked(): usedisbot = False

    def lil_changed(self):
        global caplil
        caplil = round(self.doubleSpinBoxLil.value(), 2)

    def tokken_changed(self):
        global distoken
        distoken = self.discordTokken.text()
    def channel_changed(self):
        global channel
        channel = int(self.discordChannel.text())
    def user_changed(self):
        global user
        user = int(self.discordUser.text())
    def comboBoxFunction(self):
        global mytype
        mytype = self.comboBox.currentText()

    # 텍스트 넣어주기 tI
    @pyqtSlot(str)
    def textInputTB1(self, txt):
        # print("텍스트 넣어주기 함수")
        self.mainTB1.append(txt)
        scrollbar = self.mainTB1.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # myloc runeloc 실시간 변경
    @pyqtSlot(str, str)
    def textInputLabel(self, lo, txt):
        # print("텍스트 넣어주기 함수")
        if lo == "myloc":
            self.label_myloc.setText(txt)
        elif lo == "runeloc":
            self.label_runeloc.setText(txt)
    @pyqtSlot(int)
    def deepprogress(self, val):
        self.progressBar.setValue(val)

    ### 기본 시작 매크로###
    def startMacro(self):
        global mapleOn
        global miniMap
        global ardu
        global model
        if self.isRun: self.textInputTB1("이미 실행중입니다."); return
        else:
            self.textInputTB1("시작합니다.")
            self.isRun = True
            #아두이노 사용 한다면
            if useardu:
                # 첫 시작눌렀을때 아두이노 세팅
                if self.firstMacro:
                    self.textInputTB1("아두이노 연결중")
                    try:
                        ardu = Arduino()
                        self.textInputTB1("아두이노 연결완료")
                        self.firstMacro = False
                    except:
                        self.textInputTB1("아두이노 연결 안됨")
                        self.textInputTB1("중지합니다.")
                        self.isRun = False
                        return
                # 두번째 시작을 눌렀을때
                else:
                    try:
                        self.textInputTB1("아두이노 연결 체크중")
                        ardu.release_all()
                        self.textInputTB1("아두이노 연결 완료")
                    except:
                        try:
                            ardu = Arduino()
                            self.textInputTB1("아두이노 재연결 완료")
                            self.firstMacro = False
                        except:
                            self.textInputTB1("아두이노 연결 안됨")
                            self.textInputTB1("중지합니다.")
                            self.isRun = False
                            return
            if maplecheck:
                self.textInputTB1("메이플 프로세스 확인")
                mapleOn = Capture.mapleOn(self)
                if mapleOn[4] == 0:
                    self.textInputTB1("메이플 확인 안됨")
                    self.textInputTB1("중지합니다.")
                    self.isRun = False
                    return
                # 메이플 최상위
                win32gui.SetForegroundWindow(mapleOn[4])
                bbox = mapleOn[0], mapleOn[1], mapleOn[2], mapleOn[3]
                self.label_mapleOn.setText(str(bbox))
                self.label_process.setText(str(mapleOn[4]))
                if minimapcheck:
                    self.textInputTB1("메이플 미니맵 확인")
                    screen = ImageGrab.grab(bbox)
                    # 시작 찰칵찰칵이
                    screen.save("./img/temp.png")
                    miniMap = Capture.miniMap(self, screen)
                    if miniMap[3] == 0:
                        self.textInputTB1("미니맵 인식안됨")
                        self.textInputTB1("중지합니다.")
                        self.isRun = False
                        return
                    bboxmini = miniMap[0], miniMap[1], miniMap[2], miniMap[3]
                    minisize = miniMap[2] - miniMap[0], miniMap[3] - miniMap[1]
                    self.label_minimap.setText(str(bboxmini))
                    self.label_minimapsize.setText(str(minisize))
                    infobox = 4, 15, 294, 65
                    infoimg = screen.crop(infobox)
                    infoimg.save("./img/mapinfo.png")
                    pixmap = QPixmap("./img/mapinfo.png")
                    self.label_imgmapinfo.setPixmap(pixmap)

            self.textInputTB1("캡쳐 쓰레드 시작")
            self.captureworker = CaptureWorker()
            self.captureworker.start()
            self.captureworker.textInputTB1.connect(self.textInputTB1)
            self.captureworker.textInputLabel.connect(self.textInputLabel)

            self.textInputTB1("스크립트 쓰레드 시작")
            self.scriptworker = ScriptWorker()
            self.scriptworker.start()
            self.scriptworker.textInputTB1.connect(self.textInputTB1)
            self.scriptworker.deepprogress.connect(self.deepprogress)

            if not mytype == "스크립트제작":
                if usedisbot:
                    self.textInputTB1("디스코드 쓰레드 시작")
                    self.discordworker = DiscordWorker()
                    self.discordworker.start()
                    # self.discordworker.textInputTB1.connect(self.textInputTB1)

    def closeEvent(self, event):
        quit_msg = "종료하시겠습니까??"
        reply = QMessageBox.question(self, '매크로 종료', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                ardu.release_all()
                event.accept()
            except:
                event.accept()
        else:
            event.ignore()


# 캡쳐쓰레드
class CaptureWorker(QThread):
    textInputTB1 = pyqtSignal(str)
    textInputLabel = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.capturei = 0
        self.captureldi = 0
        self.running = True

    def run(self):
        global mapleOn
        global miniMap
        global disstat
        self.bbox = (mapleOn[0], mapleOn[1], mapleOn[2], mapleOn[3])
        self.bboxMini = (miniMap[0], miniMap[1], miniMap[2], miniMap[3])

        def myloce():
            global stat
            global rune
            global disstat
            global runetime
            global screen
            if loccheck:
                screen = ImageGrab.grab(self.bbox)
                # 내위치 찾기
                crop_img = screen.crop(self.bboxMini)
                stat = Capture.myPosition(self, crop_img)
                self.textInputLabel.emit("myloc", str(stat))
                # 약 5초마다 반복 룬찾기 및 내위치
                if self.capturei == 30:
                    self.capturei = 0
                    if not mytype == "스크립트제작":
                        if runecheck:
                            self.runet = time.time()
                            if self.runet - runetime > 900:
                                rune = Capture.runePosition(self, crop_img)
                                if not rune[1] == 0:
                                    disstat = 3
                                    # self.label_status.emit("룬 찾는중")
                                    # self.label_status.setStyleSheet(
                                    #     "color: #4D69E8; border-style: solid; border-width: 2px; border-color: #54A0FF; border-radius: 10px; ")
                                    self.textInputTB1.emit("룬출현")
                                    self.textInputLabel.emit("runeloc", str(rune))
                        if ldcheck and runedeep:
                            self.captureldi += 1
                            if self.captureldi == 4:
                                self.captureldi = 0
                                print("거탐찾아용")
                                image_array = np.array(screen)
                                with tf.device('/gpu:0'):
                                    results = inference_from_model(image_array)
                                rune_screen = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                                cv2.imwrite(f'./img/rune/{int(time.time())}.jpg', rune_screen)
                                print(results)
                                if results == 0:
                                    print("아무일도 없었다")
                                elif results == 5:
                                    print("거탐출현 클릭을 하자")
                                elif results == 6:
                                    print("거탐 문자를 쓰자")
                                else:
                                    print("룬인가바")

                self.capturei += 1





        # job1 내위치 0.1초마다
        job1 = schedule.every(caplil).seconds.do(myloce)
        while self.running:
            schedule.run_pending()
            time.sleep(caplil)
        else:
            schedule.cancel_job(job1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False


# 스크립트 쓰레드
class ScriptWorker(QThread):
    textInputTB1 = pyqtSignal(str)
    deepprogress = pyqtSignal(int)
    global stat
    global rune

    def __init__(self):
        super().__init__()
        self.starttime = 0
        self.scripti = None
        self.running = True

    def run(self):
        global disstat
        global ardu
        global runetime
        global sc
        global screen
        global stat
        global model
        if not mytype == "스크립트제작":
            if runedeep:
                self.textInputTB1.emit("딥러닝 체크")
                self.deepprogress.emit(10)
                model = tf.saved_model.load(PATH_TO_MODELS)
                self.deepprogress.emit(30)
                screen = Image.open("./img/rune_ready.jpg")
                self.deepprogress.emit(40)
                image_array = np.array(screen)
                self.deepprogress.emit(50)
                try:
                    with tf.device('/gpu:0'):
                        results = inference_from_model(image_array)
                    self.deepprogress.emit(100)
                    print(results)
                    self.textInputTB1.emit("딥러닝 준비 완료")
                except:
                    self.textInputTB1.emit("딥러닝 고장")
                    self.deepprogress.emit(0)
        self.hunttime = time.time()
        self.runeloce = 0, 0
        self.scripti = 0
        while self.running:
            if not sc == None:
                # if 룬
                if mytype == "스크립트제작":
                    gotohunt(self.hunttime)
                else:
                    # 만약 룬
                    if disstat == 3:
                        # 룬로케로 룬위치 설정
                        if self.runeloce[0] == 0:
                            if not rune[1] == 0:
                                self.starttime = time.time()
                                self.runeloce = rune
                        # 룬위치 설정이 되었다면
                        # gotorune(self.runeloce)
                        # 룬 완료시
                        if 0 <= abs(stat[0] - self.runeloce[0]) < 3 and 0 <= abs(stat[1] - self.runeloce[1]) < 2:
                            print("룬 해제 3")
                            time.sleep(1)
                            print("룬 해제 2")
                            time.sleep(1)
                            print("룬 해제 1")
                            time.sleep(1)
                            print("룬 해제")
                            # 딥쁘러닝
                            if runedeep:
                                image_array = np.array(screen)
                                with tf.device('/gpu:0'):
                                    results = inference_from_model(image_array)
                                rune_screen = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                                cv2.imwrite(f'./img/rune/{int(time.time())}.jpg', rune_screen)
                                print(results)
                            # 결과 완료면
                            # 디스스텟 동작중변경
                            disstat = 1
                            # self.label_status.setText("정상동작중")
                            # self.label_status.setStyleSheet(
                            #     "color: #41E881; border-style: solid; border-width: 2px; border-color: #67E841; border-radius: 10px; ")
                            # 룬시간 초기화
                            runetime = time.time()
                            # 룬위치 초기화
                            self.runeloce = 0, 0
                            print(f"룬까는데 걸린 시간 = {runetime - self.starttime}")
                            # 사냥시간 초기화
                            self.hunttime = time.time()
                    else:
                        gotohunt(self.hunttime)
            else:
                print("스크립트가 없습니다.")
                time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False
        ardu.release_all()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
