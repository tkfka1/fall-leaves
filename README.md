# Welcome to MILF

Hi! I'm your  **MapleStory** macro. 
 **Milf is good** .


# Installation

**pyqt5**

pip install pyqt5

**cv2**

pip install opencv-python

**win32api**

pip install pypiwin32

**pil**

pip install pillow

**serial**

pip install pyserial

**discord**

pip install py-cord==2.0.0b5 **or** pip install -U git+https://github.com/Pycord-Development/pycord

**tensorflow**

pip install tensorflow-gpu

**arduino**

https://www.arduino.cc/en/software


# Reference

**pycord to use the discordBot**

https://docs.pycord.dev/en/master/#getting-started

 **Arduino keyboard modifiers**
 
https://www.arduino.cc/reference/en/language/functions/usb/keyboard/keyboardmodifiers

**keyboard test**

https://funkeys.co.kr/bbs/page.php?hid=keytest

# How to use

that`s simple

## start
- python3
> main.py

시작 button : start
중지 button : stop , have to press a lot
불러오기 button : call the script

# config.ini

## Basic

Start with information


## Set

**기본동작모드** : basic operation

**스크립트제작** : Used when making hunting scripts
>rune check does not turn on
>discord does not turn on

## Debug

**룬찾기**button : Find the deep learning runes

## Capture set

| [Capture]  | Descriptions  |
|--|--|
| **캡쳐주기** | capture cycle , 0.1~9.9 |
| **메이플체크** | will you find the process |
| **미니맵체크**  | will you find the minimap  , dependent on **메이플체크** |
| **위치체크**  | location check , dependent on **미니맵체크** |
| **룬체크** | rune check , dependent on **위치체크** |
| **룬딥러닝** | rune answer with deep learning , dependent on **룬체크**  |


## Script set

| [Script]  | Descriptions  |
|--|--|
| **아두이노 사용** | use arduino |

## Discord set
| [Capture]  | Descriptions  |
|--|--|
| **디코봇 사용** | capture cycle , 0.1~9.9 |
| **디스코드 토큰** | discordBOT tokken |
| **디스코드 채널** | use discord channel ID |
| **디스코드 유저**  | use discord user ID |


>https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications
![](https://blog.kakaocdn.net/dn/cpmPMG/btrhKsmI6jA/BPfla461JqD2m4oqT1sTj0/img.webp)
>![](https://blog.kakaocdn.net/dn/C8Wml/btrhOG4viaJ/ObVfRfAZh3sMK5ZeaIr9VK/img.webp)![](https://blog.kakaocdn.net/dn/bIxFW0/btrhLSrXBSg/TUZIKNbqTDtcKvxAmUd5g0/img.webp)![](https://blog.kakaocdn.net/dn/t6Yst/btrhN3sfwBB/sKy8qZ2LKe17LTfNXssqjk/img.webp)
>copty to TOKKEN![](https://blog.kakaocdn.net/dn/dQS0Z3/btrhMJOqYTq/v6Nd5t1rwF9akHaC4tKMBk/img.webp)
>copy to URL
>![](https://blog.kakaocdn.net/dn/bW7LSI/btrhOIab8hw/ajFrwbfrlKqAKObhUZnYzk/img.webp)
>![](https://blog.kakaocdn.net/dn/blDB9w/btrqM4w40Su/SC7VKeOVSnKTD46lCQNK40/img.png)
>![](https://blog.kakaocdn.net/dn/Q4WMV/btrqR0NW20m/GAbM040w1vQKMws1ouRYzK/img.png)



# todo

Todo

- ver 1.0  
	> ~~basic functions~~
- ver 2.0
	> Discord Notifications
	> lie detection Notifications
- ver 3.0
	> not yet




## UML diagrams

not yet sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

not yet flow chart:

```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```
