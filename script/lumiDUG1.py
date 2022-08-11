import time
global ardu



#스크립트 불러오면 실행할 말 필수!!!!!!
def hello():
    print("루미 동윗깊1 불러와짐")
    return "루미 동윗깊1 스크립트 불러옴"

# 기본 키보드마우스 제어 함수
# def press(x):
#     ardu.press(x)
# def release(x):
#     ardu.release(x)
# def release_all():
#     ardu.release_all()
# def move(x,y):
#     ardu.move(x,y)
# def bezier_move(x,y):
#     ardu.bezier_move(x,y)
# def write(x):
#     ardu.write(x)

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

#룬까기 함수 필수


def dorune():
        time.sleep(0.1)
        # if 차이x > 40:
        #     print("왼쪽으로많이 이동")
        #     ardu.release(Keymouse.RIGHT_ARROW)
        #     ardu.press(Keymouse.LEFT_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.3)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.2)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(1)
        # elif 40 > 차이x > 6:
        #     print("왼쪽 이동")
        #     ardu.release(Keymouse.RIGHT_ARROW)
        #     ardu.press(Keymouse.LEFT_ARROW)
        #     time.sleep(0.2)
        # elif 7 > 차이x > 2:
        #     print("왼쪽 조금 이동")
        #     ardu.release(Keymouse.RIGHT_ARROW)
        #     ardu.press(Keymouse.LEFT_ARROW)
        #     time.sleep(0.05)
        # elif -40 > 차이x:
        #     print("오른쪽으로많이 이동")
        #     ardu.release(Keymouse.LEFT_ARROW)
        #     ardu.press(Keymouse.RIGHT_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.3)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.2)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(1)
        # elif -7 > 차이x > -40:
        #     print("오른쪽 이동")
        #     ardu.release(Keymouse.LEFT_ARROW)
        #     ardu.press(Keymouse.RIGHT_ARROW)
        #     time.sleep(0.2)
        # elif -1 > 차이x > -7:
        #     print("오른쪽 조금 이동")
        #     ardu.release(Keymouse.LEFT_ARROW)
        #     ardu.press(Keymouse.RIGHT_ARROW)
        #     time.sleep(0.05)
        # if 차이y > 40:
        #     print("위쪽으로많이 이동")
        #     ardu.press(Keymouse.UP_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.UP_ARROW)
        # elif 40 > 차이y > 14:
        #     print("위쪽 이동")
        #     ardu.press(Keymouse.UP_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.UP_ARROW)
        # elif 15 > 차이y > 2:
        #     print("위쪽 조금 이동")
        #     ardu.press(Keymouse.UP_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.UP_ARROW)
        # elif -40 > 차이y:
        #     print("아래쪽으로많이 이동")
        #     ardu.press(Keymouse.DOWN_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.4)
        #     ardu.release(Keymouse.DOWN_ARROW)
        # elif -16 > 차이y > -40:
        #     print("아래쪽 이동")
        #     ardu.press(Keymouse.DOWN_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.4)
        #     ardu.release(Keymouse.DOWN_ARROW)
        # elif -1 > 차이y > -15:
        #     print("아래쪽 조금 이동")
        #     ardu.press(Keymouse.DOWN_ARROW)
        #     time.sleep(0.1)
        #     ardu.press(Keymouse.LEFT_ALT)
        #     time.sleep(0.1)
        #     ardu.release(Keymouse.LEFT_ALT)
        #     time.sleep(0.4)
        #     ardu.release(Keymouse.DOWN_ARROW)
        # if 0 <= abs(stat[0] - self.runeloce[0]) < 3 and 0 <= abs(stat[1] - self.runeloce[1]) < 2:
        #     ardu.release_all()
        #     print("룬 해제")
        #     ardu.press(" ")
        #     time.sleep(0.2)
        #     ardu.release(" ")
        #     self.runestack += 1
        #     time.sleep(0.1)


def gotorune(r):
    global stat
    print("룬까러간다")
    # diffY = stat[1] - r[1]
    while True:
        diffX = stat[0] - r[0]
        if diffX > 2:
            print("왼쪽누르기")
            ardu.release(RIGHT_ARROW)
            ardu.press(LEFT_ARROW)
        elif diffX < -2:
            print("오른쪽누르기")
            ardu.release(LEFT_ARROW)
            ardu.press(RIGHT_ARROW)
        else:
            print("도착")
            ardu.release_all()
            break
        time.sleep(0.1)
        # if 0 <= abs(diffX) < 3 and 0 <= abs(diffY) < 2:
        #     print("도차쿠")



# 사냥 함수 필수
def gotohunt(stat,hunttime):
    print("사냥하좌")
    print(stat, hunttime)
    time.sleep(1)
