import os

from PyQt5 import QtMultimedia
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegion
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton

from mutagen import File

"""音乐播放界面"""
class MusicGui(QWidget):
    def __init__(self, _file):
        super(MusicGui, self).__init__()
        self.file = _file
        self.GetMusicIcon()
        self.UI()
        self.Music = QUrl.fromLocalFile(_file)
        self.Content = QtMultimedia.QMediaContent(self.Music)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(100)
        self.player.setMedia(self.Content)

    def UI(self):
        self.setWindowTitle("DesktopWife-MusicPlayGui")
        self.resize(240, 135)

        self.QuitButton = QPushButton(self)
        self.QuitButton.setIcon(QIcon(".\image\MusicQuit.png"))
        self.QuitButton.setIconSize(QSize(200, 200))
        self.QuitButton.setGeometry(208, 10, 20, 20)
        QuitButtonRect = QRectF(0, 0, self.QuitButton.width(), self.QuitButton.height())
        QuitButtonPath = QPainterPath()
        QuitButtonPath.addRoundedRect(QuitButtonRect, 10, 10)
        QuitButtonPolgon = QuitButtonPath.toFillPolygon().toPolygon()
        QuitButtonRegion = QRegion(QuitButtonPolgon)
        self.QuitButton.setMask(QuitButtonRegion)
        self.QuitButton.clicked.connect(self.QuitButtonEvent)

        self.WindowMinimizedButton = QPushButton(self)
        self.WindowMinimizedButton.setIcon(QIcon(".\image\WindowMinimized.png"))
        self.WindowMinimizedButton.setIconSize(QSize(20, 20))
        self.WindowMinimizedButton.setGeometry(180, 10, 20, 20)
        WindowMinimizedButtonRect = QRectF(0, 0,  self.WindowMinimizedButton.width(), self.WindowMinimizedButton.height())
        WindowMinimizedButtonPath = QPainterPath()
        WindowMinimizedButtonPath.addRoundedRect(WindowMinimizedButtonRect, 10, 10)
        WindowMinimizedButtonPolgon = QuitButtonPath.toFillPolygon().toPolygon()
        WindowMinimizedButtonRegion = QRegion(WindowMinimizedButtonPolgon)
        self.WindowMinimizedButton.setMask(WindowMinimizedButtonRegion)
        self.WindowMinimizedButton.clicked.connect(self.SetWindowMin)

        self.MusicIconLabel = QPushButton(self)
        self.MusicIconLabel.setGeometry(20, 20, 30, 30)
        self.MusicIconLabel.setStyleSheet("color: blue;")
        if os.path.isfile(".\music\MusicIcon\MusicIcon.jpg"):
            self.MusicIconLabel.setIcon(QIcon(".\music\MusicIcon\MusicIcon.jpg"))
            self.MusicIconLabel.setIconSize(QSize(30, 30))
        else:
            self.MusicIconLabel.setText("无法提取音频图片")
            self.MusicIconLabel.setGeometry(20, 20, 120, 30)

        self.MusicNameLabel = QLabel(self)
        self.MusicNameLabel.setGeometry(20, int((self.height() - 30) / 2), 250, 30)
        self.MusicNameLabel.setStyleSheet("font-size:10px;")
        self.MusicNameLabel.setText(os.path.split(self.file)[-1])

        self.volume = QSlider(Qt.Horizontal, self)
        self.volume.setMinimum(0)
        self.volume.setMaximum(100)
        self.volume.setValue(50)
        self.volume.setTickInterval(5)
        self.volume.setTickPosition(QSlider.TicksBelow)
        self.volume.setGeometry(10, 100, 150, 30)
        self.volume.valueChanged.connect(self.VolumeNumber)

        self.VolumeNumberLabel = QLabel(f"{self.volume.value()}", self)
        self.VolumeNumberLabel.setGeometry(175, 100, 20, 20)

        self.PlayButton = QPushButton(self)
        self.PlayButton.setIcon(QIcon(".\image\stop.png"))
        self.PlayButton.setIconSize(QSize(200, 200))
        self.PlayButton.setGeometry(200, 100, 30, 30)
        self.IS_PlayMusic = False
        self.PlayButton.clicked.connect(self.PlayButtonEvent)

        # 圆角
        rect = QRectF(0, 0, self.width(), self.height())
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        polygon = path.toFillPolygon().toPolygon()
        region = QRegion(polygon)
        self.setMask(region)

    def SetWindowMin(self):
        self.setWindowState(Qt.WindowMinimized)

    def QuitButtonEvent(self):
        self.hide()
        if os.path.isfile(".\music\MusicIcon\MusicIcon.jpg"):
            os.remove(".\music\MusicIcon\MusicIcon.jpg")
        self.player.stop()

    def PlayButtonEvent(self):
        if self.IS_PlayMusic:
            self.PauseMusic()
        else:
            self.PlayMusic()

    def VolumeNumber(self):
        self.VolumeNumberLabel.setText(f"{self.volume.value()}")
        self.player.setVolume(self.volume.value())

    def GetMusicIcon(self):
        self.MusicMutagnFile = File(self.file)
        try:
            self.MusicIconData = self.MusicMutagnFile.tags['APIC:test'].data
            with open(".\music\MusicIcon\MusicIcon.jpg", "wb") as wfp:
                wfp.write(self.MusicIconData)
        except KeyError:
            pass

    def PlayMusic(self):
        self.player.play()
        self.PlayButton.setIcon(QIcon(".\image\play.png"))
        self.PlayButton.setIconSize(QSize(200, 200))
        self.IS_PlayMusic = True

    def PauseMusic(self):
        self.player.pause()
        self.PlayButton.setIcon(QIcon(".\image\stop.png"))
        self.PlayButton.setIconSize(QSize(200, 200))
        self.IS_PlayMusic = False

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
