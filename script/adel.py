import time
import random
global ardu
global hunt
hunt = 0
global timer1
global timer2
global timer3
global timer4
timer1 = 0
timer2 = 0
timer3 = 0
timer4 = 0



#스크립트 불러오면 실행할 말 필수!!!!!!
def hello():
    print("루미 동윗깊1 불러와짐")
    return "루미 동윗깊1 스크립트 불러옴"

# 기본 키보드마우스 제어 함수
def pre(x):
    ardu.press(x)
def rel(x):
    ardu.release(x)
def rel_all():
    ardu.release_all()
def move(x, y):
    ardu.move(x, y)
def bezier_move(x,y):
    ardu.bezier_move(x, y)
def write(x):
    ardu.write(x)

# 0.001초~ rand ms변환
def randtime(x):
    x = x/1000
    time.sleep(random.uniform(0.001, x))

# 0.001초 ms변환
def slepptime(x):
    x = x/1000
    time.sleep(x)

def 텔텔공():
    ## 텔텔공 6가지방법
    r = random.randrange(1,9)
    if r == 1:
        print("1")
        pre('z')
        time.sleep(0.1)
        randtime(1)
        rel('z')
        time.sleep(0.3)
        randtime(1)
        pre(LEFT_CTRL)
        time.sleep(0.1)
        randtime(2)
        rel(LEFT_CTRL)
        randtime(1)
    elif r == 2:
        print("2")
        pre('z')
        time.sleep(0.2)
        randtime(1)
        time.sleep(0.1)
        rel('z')
        randtime(2)
        time.sleep(0.4)
        pre(LEFT_CTRL)
        time.sleep(0.1)
        randtime(1)
        rel(LEFT_CTRL)
        randtime(1)
    elif r == 3:
        print("3")
        pre('z')
        time.sleep(0.1)
        randtime(2)
        time.sleep(0.1)
        randtime(1)
        pre(LEFT_CTRL)
        randtime(1)
        time.sleep(0.3)
        rel('z')
        randtime(3)
        time.sleep(0.2)
        rel(LEFT_CTRL)
        randtime(1)
    elif r == 4:
        print("4")
        randtime(1)
        pre(LEFT_CTRL)
        time.sleep(0.1)
        randtime(1)
        pre('z')
        time.sleep(0.1)
        randtime(1)
        time.sleep(0.3)
        randtime(1)
        rel('z')
        randtime(1)
        time.sleep(0.3)
        rel(LEFT_CTRL)
        randtime(2)
    elif r == 5:
        print("5")
        randtime(1)
        pre(LEFT_CTRL)
        time.sleep(0.5)
        randtime(2)
        pre('z')
        time.sleep(0.1)
        randtime(1)
        time.sleep(0.1)
        randtime(1)
        randtime(2)
        rel(LEFT_CTRL)
        time.sleep(0.2)
        randtime(1)
        rel('z')
    elif r == 6:
        print("6")
        randtime(1)
        randtime(1)
        randtime(2)
        pre('z')
        time.sleep(0.1)
        randtime(1)
        pre(LEFT_CTRL)
        time.sleep(0.1)
        randtime(1)
        randtime(2)
        rel(LEFT_CTRL)
        time.sleep(0.2)
        randtime(1)
        time.sleep(0.1)
        randtime(1)
        time.sleep(0.1)
        randtime(1)
        randtime(2)
        time.sleep(0.2)
        randtime(1)
        rel('z')
    elif r == 7:
        print("7")
        randtime(1)
        randtime(1)
        pre('z')
        time.sleep(0.1)
        randtime(1)
        pre(LEFT_CTRL)
        time.sleep(0.1)
        randtime(2)
        rel(LEFT_CTRL)
        time.sleep(0.2)
        randtime(1)
        time.sleep(0.1)
        randtime(2)
        time.sleep(0.2)
        randtime(1)
        rel('z')
    else:
        print("8")
        pre('z')
        time.sleep(0.2)
        randtime(1)
        randtime(1)
        time.sleep(0.1)
        pre(LEFT_CTRL)
        time.sleep(0.1)
        randtime(2)
        rel(LEFT_CTRL)
        time.sleep(0.3)
        randtime(1)
        rel('z')
        randtime(1)



def 윗점():
    ## 윗점 3가지방법
    r = random.randrange(1,5)
    if r == 1:
        pre('c')
        randtime(1)
        randtime(2)
        randtime(1)
        randtime(3)
        rel('c')
        time.sleep(2)
        randtime(2)
        randtime(1)
        randtime(3)
    elif r == 2:
        pre(UP_ARROW)
        randtime(2)
        randtime(1)
        randtime(3)
        pre(LEFT_ALT)
        randtime(2)
        randtime(1)
        randtime(2)
        randtime(1)
        rel(LEFT_ALT)
        randtime(1)
        randtime(3)
        randtime(2)
        randtime(1)
        pre(LEFT_ALT)
        randtime(2)
        randtime(1)
        randtime(3)
        randtime(1)
        rel(LEFT_ALT)
        randtime(1)
        randtime(1)
        randtime(1)
        randtime(2)
        pre('z')
        randtime(1)
        randtime(2)
        rel('z')
        randtime(1)
        randtime(2)
        rel(UP_ARROW)
    elif r == 3:
        pre(UP_ARROW)
        randtime(1)
        randtime(2)
        randtime(1)
        pre(LEFT_ALT)
        randtime(1)
        randtime(3)
        randtime(2)
        randtime(1)
        rel(LEFT_ALT)
        randtime(1)
        randtime(2)
        randtime(1)
        randtime(1)
        pre(LEFT_ALT)
        randtime(1)
        randtime(2)
        randtime(1)
        randtime(1)
        rel(LEFT_ALT)
        randtime(1)
        randtime(2)
        randtime(2)
        randtime(3)
        pre('z')
        randtime(1)
        randtime(2)
        rel('z')
        randtime(1)
        randtime(2)
        rel(UP_ARROW)
    elif r == 4:
        pre(UP_ARROW)
        randtime(1)
        randtime(1)
        randtime(1)
        pre(LEFT_ALT)
        randtime(3)
        randtime(2)
        randtime(1)
        randtime(2)
        rel(LEFT_ALT)
        randtime(1)
        randtime(1)
        randtime(1)
        randtime(1)
        pre(LEFT_ALT)
        randtime(1)
        randtime(1)
        randtime(1)
        randtime(1)
        pre('z')
        randtime(1)
        randtime(2)
        rel(LEFT_ALT)
        randtime(1)
        randtime(1)
        randtime(1)
        rel(UP_ARROW)
        randtime(3)
        randtime(2)
        randtime(1)
        rel('z')
        randtime(1)
        randtime(1)

    else:
        pre('c')
        randtime(2)
        randtime(1)
        randtime(3)
        randtime(2)
        randtime(1)
        randtime(2)
        randtime(1)
        randtime(2)
        randtime(1)
        randtime(2)
        rel('c')
        time.sleep(2)
        randtime(3)

def 한칸텔텔공():
    print("한칸텔텔공격")
    randtime(50)
    pre(LEFT_CTRL)
    randtime(10)
    pre('z')
    randtime(50)
    slepptime(200)
    randtime(50)
    rel(LEFT_CTRL)
    slepptime(200)
    randtime(50)
    rel('z')
    slepptime(100)
def 두칸텔텔공():
    print("두칸")
    randtime(50)
    pre(LEFT_CTRL)
    randtime(10)
    pre('z')
    randtime(150)
    rel(LEFT_CTRL)
    slepptime(300)
    randtime(50)
    slepptime(300)
    randtime(50)
    rel('z')
    slepptime(300)


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
def gotohunt(hunttime):
    global stat
    global hunt
    global timer1
    global timer2
    global timer3
    global timer4
    x = stat[0]
    y = stat[1]

    # 사냥 처음 시작한다면
    if hunt == 0:
        hunt = 1
        timer1 = time.time()
        timer2 = time.time()
        timer3 = time.time()
        timer4 = time.time()

    elif hunt == 1:
        t1 = timer1 - hunttime
        t2 = timer2 - hunttime
        t3 = timer3 - hunttime
        t4 = timer4 - hunttime
        ti = time.time() - hunttime
        print(ti)
        ran = random.randrange(1,1001)
        if ran == 1000:
            print("병신짓")
        elif 911 > ran > 900:
            pre('q')
            randtime(10)
            rel('q')
            randtime(10)
        elif 921 > ran > 910:
            pre('d')
            randtime(10)
            rel('d')
            randtime(10)
        elif 926 > ran > 920:
            pre('0')
            randtime(10)
            rel('0')
            randtime(10)
        else:
            #동윗깊 위치
            # 만약 위치
            if y < 25:
                if x > 192:
                    print("왼쪽")
                    rel(RIGHT_ARROW)
                    randtime(10)
                    pre(LEFT_ARROW)
                    randtime(10)
                elif x < 38:
                    print("오른쪽")
                    rel(LEFT_ARROW)
                    randtime(10)
                    pre(RIGHT_ARROW)
                    randtime(10)
                if 55 > x or x > 185:
                    한칸텔텔공()
                else:
                    두칸텔텔공()
            else:
                randtime(400)
                print("공격아랫")
                pre(LEFT_CTRL)
                randtime(100)
                pre('z')
                randtime(100)
                randtime(400)
                randtime(100)
                randtime(400)
                rel(LEFT_CTRL)
                randtime(100)
                randtime(400)
                randtime(400)
                rel('z')
                randtime(100)





# 동윗깊1
# 맨윗줄 y 20
# 오른상단 x 209 146
# 가운상단 x 138 92 y 20
# 왼상단 x 86 22