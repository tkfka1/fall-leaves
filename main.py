import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import data.arduLeo

form_class = uic.loadUiType("mainWindow.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
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
        self.textInputTB1("중지합니다.")

    def onReloadClicked(self):
        # print("load 버튼")
        self.textInputTB1("스크립트를 불러옵니다.")

    def chkFunction(self):
        # 무한반복
        if self.checkBox1.isChecked(): print("무한반복 체크")
        if not self.checkBox1.isChecked(): print("무한반복 미체크")

        # 룬체크
        if self.checkBox2.isChecked(): print("룬체크안함 체크")
        if not self.checkBox2.isChecked(): print("룬체크안함 미체크")

    # 텍스트 넣어주기 tI
    def textInputTB1(self, txt):
        # print("텍스트 넣어주기 함수")
        self.mainTB1.append(txt)
        scrollbar = self.mainTB1.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    ### 기본 시작 매크로###
    def startMacro(self):
        print("매크로시작")
        print("아두이노 확인")
        arduino = data.arduLeo.Arduino()
        print(arduino)
        arduino.move(300, 300)
        print("메이플 프로세스확인")
        print("메이플 미니맵 확인")
        print("내 위치 확인")
        print("딥러닝체크")
        print("스크립트 불러오기")
        print("스크립트 시작")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
