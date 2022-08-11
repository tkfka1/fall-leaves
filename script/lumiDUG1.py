import time
global ardu
#스크립트 불러오면 실행할 말 필수!!!!!!
def hello():
    print("루미 동윗깊1 불러와짐")
    return "루미 동윗깊1 스크립트 불러옴"

def press(x):
    ardu.press(x)
def release(x):
    ardu.release(x)
def move(x,y):
    ardu.move(x,y)
def bezier_move(x,y):
    ardu.bezier_move(x,y)
def write(x):
    ardu.write(x)
def gotorune(stat, runeloce):
    print("룬까러가장")
    print(stat, runeloce)
    time.sleep(1)
    # 차이x = stat[0] - self.runeloce[0]
    # 차이y = stat[1] - self.runeloce[1]
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

def gotohunt(stat,hunttime):
    print("사냥하좌")
    print(stat, hunttime)
    time.sleep(1)
