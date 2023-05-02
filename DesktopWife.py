import sys
# import os

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
# from PyQt5.QtWidgets import QFileDialog
# from PyQt5.QtWidgets import QMessageBox

import WeatherGui
import Tray
import VoiceToText
import ProgramLog
import ProgramsConfigWindow

LOG = ProgramLog.ProgramLog()

VoiceToText.run()


class DesktopWife(QWidget):
    """
    Main Window
    """

    def __init__(self):
        super(DesktopWife, self).__init__()
        self.m_flag = False
        self.m_Position = None
        self.Image = QPixmap(".\\image\\bss.png")
        self.WindowSize = QDesktopWidget().screenGeometry()

        self.setWindowTitle("DesktopWife")
        self.resize(int(self.Image.width()), int(self.Image.height()))
        self.move(
            int((self.WindowSize.width() - self.Image.width()) / 2),
            int((self.WindowSize.height() - self.Image.height()) / 2)
        )
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.PlayLabel = QLabel(self)
        self.PlayLabel.setPixmap(self.Image)

        self.WindowMessage = QLabel("我好困~", self)
        self.WindowMessage.setGeometry(int((self.Image.width() - 10) / 10) + 10, 10, 800, 40)
        self.WindowMessage.setStyleSheet("color: white;")

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._WindowMenu)

        self.Timer = QTimer()
        self.Timer.start(5000)
        self.Timer.timeout.connect(self.RandomWindowMessage)

        self._Tray = Tray.TrayIcon(self)
        self.WeatherForecastGUI = WeatherGui.WeatherGUI()


    def _WindowMenu(self) -> None:
        """
        右键菜单
        :return: None
        """
        self.Menu = QMenu(self)
        self.Menu.setStyleSheet("background-color: black; color: white;")

        self.WeatherForecastQAction = QAction(QIcon(".\\image\\Button.png"), u"查看天气", self)
        self.Menu.addAction(self.WeatherForecastQAction)

        self.ConfigQAction = QAction(QIcon(".\\image\\Button.png"), u"配置", self)
        self.Menu.addAction(self.ConfigQAction)

        self.StartTray = QAction(QIcon(".\\image\\bs_icon.png"), u"退置托盘", self)
        self.Menu.addAction(self.StartTray)

        self.CloseWindowAction = QAction(QIcon(".\\image\\Quit.png"), u"退出程序", self)
        self.Menu.addAction(self.CloseWindowAction)

        self.WeatherForecastQAction.triggered.connect(self.WeatherForecast)
        self.ConfigQAction.triggered.connect(self.ProgramsConfig)
        self.StartTray.triggered.connect(self.SetTray)
        self.CloseWindowAction.triggered.connect(self.CloseWindowActionEvent)

        self.Menu.popup(QCursor.pos())

        # 圆角
        rect = QRectF(0, 0, self.Menu.width(), self.Menu.height())
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        polygon = path.toFillPolygon().toPolygon()
        region = QRegion(polygon)
        self.Menu.setMask(region)

    def ProgramsConfig(self) -> None:
        """
        设置界面
        :return: None
        """
        self.ConfigWindow = ProgramsConfigWindow.main()
        self.ConfigWindow.show()

    def CloseWindowActionEvent(self) -> None:
        """
        关闭界面并提出后台进程
        :return: None
        """
        self.close()
        VoiceToText.CONTROLLER = False
        exit(0)

    def SetTray(self) -> None:
        """
        系统托盘
        :return: None
        """
        self._Tray.show()
        self.hide()

    def RandomWindowMessage(self) -> None:
        """
        获取机器人回答，同步到右上角位置
        :return: None
        """
        self.WindowMessage.setText(VoiceToText.RETURNTEXT)

    def WeatherForecast(self) -> None:
        """
        天气预报功能
        :return: None
        """
        self.WeatherForecastGUI.show()

    def mousePressEvent(self, event) -> None:
        """
        重写移动事假，更改鼠标图标
        :param event:
        :return:
        """
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent) -> None:
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent) -> None:
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = DesktopWife()
    Window.show()
    app.exec_()
