import ctypes
import cv2
import numpy as np
import win32gui
import win32con
import win32ui
from ctypes import windll
from PIL import ImageGrab , Image

MyPos_templ = cv2.imread('./data/img/My_Position.png', cv2.IMREAD_COLOR)
MyPos_templ_mask = cv2.imread('./data/img/My_Position_mask.png', cv2.IMREAD_COLOR)
Rune_templ = cv2.imread('./data/img/Is_Rune.png', cv2.IMREAD_COLOR)
Rune_templ_mask = cv2.imread('./data/img/Is_Rune_mask.png', cv2.IMREAD_COLOR)
Rune_Check_templ = cv2.imread('./data/img/Rune_Check.png', cv2.IMREAD_COLOR)


# 메이플 켜져있나 확인
def mapleOn():
    hwnd = win32gui.FindWindow(None, "MapleStory")
    if hwnd >=1:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        result =  left +3, top + 26 , left + 3 + 1366 , top + 26 + 768, hwnd
    else:
        # left , top , right , bot , hwnd
        result = 0 , 0 , 0 , 0 , 0
    return result


def miniMap(img):
    img = img.crop((0, 0, 500, 500))
    img11 = cv2.imread('./data/img/minimapLU.png', cv2.IMREAD_COLOR)
    res_pos1 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)),img11, cv2.TM_CCORR_NORMED)
    con_pos1 = res_pos1.max()
    loc_pos1 = np.where(res_pos1 == con_pos1)

    img22 = cv2.imread('./data/img/minimapRD.png', cv2.IMREAD_COLOR)
    res_pos2 = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)),img22, cv2.TM_CCORR_NORMED)
    con_pos2 = res_pos2.max()
    loc_pos2 = np.where(res_pos2 == con_pos2)
    img.save("./data/img/tempmini.png")
    if con_pos1 > 0.95 and con_pos2 > 0.95:
        return loc_pos1[1][0]+1, loc_pos1[0][0]+1, loc_pos2[1][0]+12, loc_pos2[0][0]+11 , con_pos1, con_pos2
    else:
        return 0, 0, 0, 0 ,con_pos1, con_pos2

# 메이플 숨겨졌을 때 활성화하고 최상위
def mapleTop(hwnd):
    # win32gui.SetForegroundWindow(hwnd)
    ctypes.windll.user32.ShowWindowAsync(hwnd, win32con.SW_SHOWNORMAL)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    #win32gui.SetWindowPos(hwnd,win32con.HWND_NOTOPMOST,0,0,0,0,win32con.SWP_NOSIZE)

def myPosition(img):
    try:
        res_mypos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), MyPos_templ, cv2.TM_CCORR_NORMED, mask=MyPos_templ_mask)
        con_mypos = res_mypos[res_mypos <= 1].max()
        loc_mypos = np.where(res_mypos == con_mypos)
        return loc_mypos[1][0], loc_mypos[0][0]
    except:
        return 0, 0

def runePosition(img):
    try:
        res_runepos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Rune_templ, cv2.TM_CCORR_NORMED, mask=Rune_templ_mask)
        con_runepos = res_runepos[res_runepos < 1].max()
        loc_runepos = np.where(res_runepos == con_runepos)
        return loc_runepos[1][0], loc_runepos[0][0], con_runepos
    except:
        return 0, 0






def capAll(hwnd):
    """
    메이플에서 채팅창 밖으로 빼기가 있다면 2개의 같은 이름의 프로세스로 된다.
    hwnd = win32gui.FindWindow(None, 'MapleStory')
    print(hwnd)
    """
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    #메이플 특성 가로 -6 세로 -40을 해야 빈화면없이 제대로 잘린다
    saveBitMap.CreateCompatibleBitmap(mfcDC, w-6, h-40)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("test.png")

    return result


def capAllReturn(hwnd):
    """
    메이플에서 채팅창 밖으로 빼기가 있다면 2개의 같은 이름의 프로세스로 된다.
    hwnd = win32gui.FindWindow(None, 'MapleStory')
    print(hwnd)
    """
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    #메이플 특성 가로 -6 세로 -40을 해야 빈화면없이 제대로 잘린다
    saveBitMap.CreateCompatibleBitmap(mfcDC, w-6, h-40)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("test.png")
        return im


def capReturn(hwnd, w, h):
    """
    w 가로 h 세로
    """
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    #메이플 특성 가로 -6 세로 -40을 해야 빈화면없이 제대로 잘린다
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # PrintWindow Succeeded
        return im
    else:
        return False


def capReturn2(hwnd, w, h):
    """
    w 가로 h 세로
    """
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    #메이플 특성 가로 -6 세로 -40을 해야 빈화면없이 제대로 잘린다
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("test.png")
        return im


def cropImg(img, x):
    crop_img = img.crop(x)
    return crop_img





# 숨겨졌을 때 활성화
def hideActive(hwnd):
    ctypes.windll.user32.ShowWindowAsync(hwnd, win32con.SW_SHOWNORMAL)


# 메이플 숨겨졌을 때 활성화하고 최상위
def mapleActive(hwnd):
    ctypes.windll.user32.ShowWindowAsync(hwnd, win32con.SW_SHOWNORMAL)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    #win32gui.SetWindowPos(hwnd,win32con.HWND_NOTOPMOST,0,0,0,0,win32con.SWP_NOSIZE)






# 현재 프로세스 찾기
def getWindowList():
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
            hwnd_list.append((title, hwnd))
        return True

    output = []
    win32gui.EnumWindows(callback, output)
    return output

# 메이플 프로세스 번호 찾기(채팅창 있어도 가능)
def getWindowMaple(i):
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
            if title == 'MapleStory':
                hwnd_list.append(hwnd)
        return True

    output = []
    win32gui.EnumWindows(callback, output)
    if len(output) == 2:
        if i == 0:
            result = output[1]
        else:
            result = output[0]
    else:
        result = output[0]
    return result












# def getWindowMaple():
#     def callback(hwnd, hwnd_list: list):
#         title = win32gui.GetWindowText(hwnd)
#         if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
#             if title == 'MapleStory':
#                 hwnd_list.append(hwnd)
#         return True
#     output = []
#     win32gui.EnumWindows(callback, output)
#     if len(output) == 2:
#         result = output[1]
#     else:
#         result = output[0]
#     return result
#
# def capAllMaple():
#     """
#     메이플에서 채팅창 밖으로 빼기가 있다면 2개의 같은 이름의 프로세스로 된다.
#     hwnd = win32gui.FindWindow(None, 'MapleStory')
#     print(hwnd)
#     """
#     hwnd = getWindowMaple()
#     print(hwnd)
#     # Change the line below depending on whether you want the whole window
#     # or just the client area.
#     #left, top, right, bot = win32gui.GetClientRect(hwnd)
#     left, top, right, bot = win32gui.GetWindowRect(hwnd)
#     w = right - left
#     h = bot - top
#
#     hwndDC = win32gui.GetWindowDC(hwnd)
#     mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
#     saveDC = mfcDC.CreateCompatibleDC()
#
#     saveBitMap = win32ui.CreateBitmap()
#     #메이플 특성 가로 -6 세로 -40을 해야 빈화면없이 제대로 잘린다
#     saveBitMap.CreateCompatibleBitmap(mfcDC, w-6, h-40)
#
#     saveDC.SelectObject(saveBitMap)
#
#     # Change the line below depending on whether you want the whole window
#     # or just the client area.
#     result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
#     #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
#     print(result)
#
#     bmpinfo = saveBitMap.GetInfo()
#     bmpstr = saveBitMap.GetBitmapBits(True)
#
#     im = Image.frombuffer(
#         'RGB',
#         (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
#         bmpstr, 'raw', 'BGRX', 0, 1)
#
#     win32gui.DeleteObject(saveBitMap.GetHandle())
#     saveDC.DeleteDC()
#     mfcDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, hwndDC)
#
#     if result == 1:
#         #PrintWindow Succeeded
#         im.save("test.png")
