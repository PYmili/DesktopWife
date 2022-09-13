import sys
import os

from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QRegion
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import requests

import WeatherGui
import MusicPlayer
import Tray
import VoiceToText

VoiceToText.run()

"""主界面"""
class DesktopWife(QWidget):
    def __init__(self):
        super(DesktopWife, self).__init__()
        self.UI()

    def UI(self):
        self.Image = QPixmap(".\image\\bg.png")
        self.WindowSize = QDesktopWidget().screenGeometry()

        self.setWindowTitle("DesktopWife")
        self.resize(int(self.Image.width()), int(self.Image.height()))
        self.move(int((self.WindowSize.width() - self.Image.width()) / 2), int((self.WindowSize.height() - self.Image.height()) / 2))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.PlayLabel = QLabel(self)
        self.PlayLabel.setPixmap(self.Image)

        self.WindowMessage = QLabel("我好困", self)
        self.WindowMessage.setGeometry(int((self.Image.width() - 80) / 2) + 10, 10, 200, 40)
        self.WindowMessage.setStyleSheet("color: white;")

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._WindowMenu)

        self.Timer = QTimer()
        self.Timer.start(5000)
        self.Timer.timeout.connect(self.RandomWindowMessage)

    """右键菜单"""
    def _WindowMenu(self):
        self.Menu = QMenu(self)
        self.Menu.setStyleSheet("background-color: black; color: white;")

        self.WeatherForecastQAction = QAction(QIcon(".\image\Button.png"), u"查看天气", self)
        self.Menu.addAction(self.WeatherForecastQAction)

        self.PlayMusicQAction = QAction(QIcon(".\image\Button.png"), u"播放音乐", self)
        self.Menu.addAction(self.PlayMusicQAction)

        self.StartTray = QAction(QIcon(".\image\\bg.png"), u"退置托盘", self)
        self.Menu.addAction(self.StartTray)

        self.CloseWindowAction = QAction(QIcon(".\image\Quit.png"), u"退出程序", self)
        self.Menu.addAction(self.CloseWindowAction)

        self.WeatherForecastQAction.triggered.connect(self.WeatherForecast)
        self.PlayMusicQAction.triggered.connect(self.MusicPaly)
        self.StartTray.triggered.connect(self.SetTray)
        self.CloseWindowAction.triggered.connect(self.ColseWindowActionEvent)

        self.Menu.popup(QCursor.pos())

        # 圆角
        rect = QRectF(0, 0, self.Menu.width(), self.Menu.height())
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        polygon = path.toFillPolygon().toPolygon()
        region = QRegion(polygon)
        self.Menu.setMask(region)

    def ColseWindowActionEvent(self):
        VoiceToText._conent = False
        self.close()
        sys.exit()

    """系统托盘"""
    def SetTray(self):
        self._Tray = Tray.TrayIcon(self)
        self._Tray.show()
        self.hide()

    """随机一诗"""
    def RandomWindowMessage(self):
        GET = requests.get(
            "https://v2.jinrishici.com/one.json?client=browser-sdk/1.2&X-User-Token=cPR5KO5BS5tEI%2BCI%2Fk4e0mxDgRFHS4qM",
            proxies={
                "http": "http://117.169.113.109/",
            })
        if GET.status_code == 200:
            self.WindowMessage.setText("，\n".join(GET.json()['data']['content'].split("，")))
        else:
            return False

    """音乐播放"""
    def MusicPaly(self):
        self.file, _Type = QFileDialog.getOpenFileName(self, u"选择音乐文件", f"{os.path.split(__file__)[0]}\\music")
        if os.path.isfile(self.file):
            self._MusicPlayGui = MusicPlayer.MusicGui(self.file)
            self._MusicPlayGui.show()
        else:
            QMessageBox.information(self, "提示", f"文件：{self.file} 无法识别")

    """天气预报"""
    def WeatherForecast(self):
        self.WeatherForecastGUI = WeatherGui.WeatherGUI()
        self.WeatherForecastGUI.show()

    """重写移动事假，更改鼠标图标"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = DesktopWife()
    Window.show()
    app.exec_()