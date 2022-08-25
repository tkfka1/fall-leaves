import time

import cv2
import numpy as np
from PIL import ImageGrab, Image

MyPos_templ = cv2.imread('./img/My_Position.png', cv2.IMREAD_COLOR)
MyPos_templ_mask = cv2.imread('./img/My_Position_mask.png', cv2.IMREAD_COLOR)
Rune_templ = cv2.imread('./img/Is_Rune.png', cv2.IMREAD_COLOR)
Rune_templ_mask = cv2.imread('./img/Is_Rune_mask.png', cv2.IMREAD_COLOR)
Rune_Check_templ = cv2.imread('./img/Rune_Check.png', cv2.IMREAD_COLOR)
MiniLU = cv2.imread('./img/minimapLU.png', cv2.IMREAD_COLOR)
MiniRD = cv2.imread('./img/minimapRD.png', cv2.IMREAD_COLOR)
MiniLU_mask = cv2.imread('./img/minimapLU_mask.png', cv2.IMREAD_COLOR)
MiniRD_mask = cv2.imread('./img/minimapRD_mask.png', cv2.IMREAD_COLOR)


def runePosition(img):
    try:
        # res_runepos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), Rune_templ,
        #                                 cv2.TM_CCORR_NORMED, mask=Rune_templ_mask)
        res_runepos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), MyPos_templ, cv2.TM_SQDIFF, mask=MyPos_templ_mask)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res_runepos)
        con_runepos = minVal
        loc_runepos = minLoc
        # img.save("./img/tempmini.png")
        # print(loc_runepos[0], loc_runepos[1], con_runepos)
        print(minVal, maxVal, minLoc, maxLoc)
        return loc_runepos[1][0], loc_runepos[0][0]
    except:
        return 0, 0

def mapinfo(im1):
    try:
        infobox = 4, 15, 294, 65
        crop_img = im1.crop(infobox)
        mapinfoimg = cv2.imread('./img/mapinfo.png', cv2.IMREAD_COLOR)
        res_map = cv2.matchTemplate((cv2.cvtColor(np.array(crop_img), cv2.COLOR_RGB2BGR)), mapinfoimg, cv2.TM_SQDIFF_NORMED)
        con_map = res_map.min()
        if con_map < 0.01:
            return 0
        else:
            return 1
    except:
        return 2


def mapinfo2(img):
    try:
        crop_img = img.crop(4, 15, 294, 65)
        res_runepos = cv2.matchTemplate((cv2.cvtColor(np.array(crop_img), cv2.COLOR_RGB2BGR)), mapinfoimg, cv2.TM_SQDIFF)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res_runepos)
        con_map = minVal
        print(con_map)
        return 0,0
    except:
        return 0, 0


a = time.time()
bbox = 0,0,400,400
bboxMini = 0,0,300,300
infobox = 4, 15, 294, 65
# screen = ImageGrab.grab(bbox)
# # 내위치 찾기
# crop_img = screen.crop(bboxMini)
im = Image.open("./img/temp.png")
rune = mapinfo(im)
print(rune)
print(time.time()-a)
# TM_CCOEFF 163 206 0.829047
# TM_CCORR_NORMED 201 101 0.8486633
# TM_SQDIFF 100 200 0.0
# TM_SQDIFF_NORMED 100 200 0.00.035032033920288086
