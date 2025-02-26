from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QTimer,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon, QFontDatabase, QDragEnterEvent, 
    QDropEvent, QImage, QKeySequence, QLinearGradient, QPainter, QMovie,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSlider, QFileDialog,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import res
import os


# Nuevos temas con colores pasteles
pastel_light_theme = """
    QWidget {
        background-color: #F6F6F2;
        color: #2D3142;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 11pt;
    }
    QLabel {
        color: #2D3142;
    }
    QPushButton {
        background-color: #D8E2DC;
        color: #2D3142;
        border-radius: 5px;
        padding: 4px;
        border: none;
    }
    QPushButton:hover {
        background-color: #FFD6BA;
    }
    QPushButton:pressed {
        background-color: #A9B8C2;
    }
    QSlider::groove:horizontal {
        border-radius: 3px;
        height: 6px;
        background-color: #E8E9EB;
    }
    QSlider::handle:horizontal {
        background-color: #FEC89A;
        border-radius: 8px;
        width: 16px;
        margin: -5px 0;
    }
    QSlider::handle:horizontal:hover {
        background-color: #E8A87C;
    }
    #header, #footer {
        background-color: #FADFD9;
    }
    #mainBody {
        background-color: #F6F6F2;
    }
    #currentChordBtn {
        background-color: #FEC89A;
        font-size: 24pt;
    }
    #prevChordBtn, #nxtChordBtn {
        background-color: #FFD6BA;
        font-size: 20pt;
    }
    #prePrevChordBtn, #postNxtChordBtn {
        background-color: #F8EDEB;
        font-size: 16pt;
    }
    #keyLabel {
        font-size: 14pt;
        font-weight: bold;
        color: #2D3142;
    }
    #appNameLabel {
        font-family: 'Segoe UI Semibold', Arial, sans-serif;
        font-size: 16pt;
        color: #2D3142;
    }
"""

pastel_dark_theme = """
    QWidget {
        background-color: #2D3142;
        color: #F6F6F2;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 11pt;
    }
    QLabel {
        color: #F6F6F2;
    }
    QPushButton {
        background-color: #4F5D75;
        color: #F6F6F2;
        border-radius: 5px;
        padding: 4px;
        border: none;
    }
    QPushButton:hover {
        background-color: #BFC0C0;
        color: #2D3142;
    }
    QPushButton:pressed {
        background-color: #A9B8C2;
    }
    QSlider::groove:horizontal {
        border-radius: 3px;
        height: 6px;
        background-color: #4F5D75;
    }
    QSlider::handle:horizontal {
        background-color: #A9B8C2;
        border-radius: 8px;
        width: 16px;
        margin: -5px 0;
    }
    QSlider::handle:horizontal:hover {
        background-color: #E8A87C;
    }
    #header, #footer {
        background-color: #41506B;
    }
    #mainBody {
        background-color: #2D3142;
    }
    #currentChordBtn {
        background-color: #E8A87C;
        color: #2D3142;
        font-size: 24pt;
    }
    #prevChordBtn, #nxtChordBtn {
        background-color: #C38D9E;
        font-size: 20pt;
    }
    #prePrevChordBtn, #postNxtChordBtn {
        background-color: #4F5D75;
        font-size: 16pt;
    }
    #keyLabel {
        font-size: 14pt;
        font-weight: bold;
        color: #F6F6F2;
    }
    #appNameLabel {
        font-family: 'Segoe UI Semibold', Arial, sans-serif;
        font-size: 16pt;
        color: #F6F6F2;
    }
"""


class SeekSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            value = self.minimum() + ((self.maximum() - self.minimum()) * event.x()) / self.width()
            self.setValue(int(value))
            self.sliderMoved.emit(int(value))
        super().mousePressEvent(event)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        
        # Aumentar el tamaño de la ventana en un 100%
        MainWindow.resize(896, 810)  # Duplicado del tamaño original (448, 405)
        MainWindow.setStyleSheet(pastel_light_theme)  # Usar el tema pastel claro por defecto
        
        self.centralwidget = QWidget(MainWindow)
        
        # Cargar las fuentes personalizadas
        QFontDatabase.addApplicationFont(":/fonts/here-be-dubstep-font/HereBeDubstepRegular-JDaB.ttf")
        
        # Configurar fuentes adicionales para un mejor aspecto musical
        font_id = QFontDatabase.addApplicationFont(":/fonts/the-score-font/TheScoreNormal-BWpx.ttf")
        if font_id >= 0:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.musical_font = QFont(font_family, 14)
        else:
            # Fuente de respaldo si no se puede cargar la fuente musical
            self.musical_font = QFont("Arial", 14)
        
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QWidget(self.centralwidget)
        self.header.setObjectName(u"header")
        self.horizontalLayout_3 = QHBoxLayout(self.header)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.appIconLabel = QLabel(self.header)
        self.appIconLabel.setObjectName(u"appIconLabel")
        self.appIconLabel.setMaximumSize(QSize(48, 48))  # Aumentado el tamaño del icono
        self.appIconLabel.setPixmap(QPixmap(u":/icons/chord.png").scaled(48, 48, Qt.KeepAspectRatio))

        self.horizontalLayout_3.addWidget(self.appIconLabel)

        self.appNameLabel = QLabel(self.header)
        self.appNameLabel.setObjectName(u"appNameLabel")
        # Configurar una fuente más atractiva para el título
        title_font = QFont("Segoe UI Semibold", 18)
        self.appNameLabel.setFont(title_font)

        self.horizontalLayout_3.addWidget(self.appNameLabel, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.headerSpacerMain = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.headerSpacerMain)

        self.themeBtn = QPushButton(self.header)
        self.themeBtn.setObjectName(u"themeBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.themeBtn.sizePolicy().hasHeightForWidth())
        self.themeBtn.setSizePolicy(sizePolicy)
        self.themeBtn.setMinimumSize(QSize(0, 32))  # Aumentado
        icon = QIcon()
        icon.addFile(u":/icons/sun.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.themeBtn.setIcon(icon)
        self.themeBtn.setIconSize(QSize(24, 24))  # Aumentado

        self.horizontalLayout_3.addWidget(self.themeBtn, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.headerSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.headerSpacer2)

        self.appControlWidget = QWidget(self.header)
        self.appControlWidget.setObjectName(u"appControlWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.appControlWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimizeBtn = QPushButton(self.appControlWidget)
        self.minimizeBtn.setObjectName(u"minimizeBtn")
        self.minimizeBtn.setMinimumSize(QSize(40, 40))  # Aumentado
        self.minimizeBtn.setMaximumSize(QSize(40, 40))  # Aumentado
        icon1 = QIcon()
        icon1.addFile(u":/icons/minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeBtn.setIcon(icon1)
        self.minimizeBtn.setIconSize(QSize(24, 24))  # Aumentado

        self.horizontalLayout_2.addWidget(self.minimizeBtn, 0, Qt.AlignRight|Qt.AlignTop)

        self.closeBtn = QPushButton(self.appControlWidget)
        self.closeBtn.setObjectName(u"closeBtn")
        self.closeBtn.setMinimumSize(QSize(40, 40))  # Aumentado
        self.closeBtn.setMaximumSize(QSize(40, 40))  # Aumentado
        icon2 = QIcon()
        icon2.addFile(u":/icons/x.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.closeBtn.setIcon(icon2)
        self.closeBtn.setIconSize(QSize(24, 24))  # Aumentado

        self.horizontalLayout_2.addWidget(self.closeBtn, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_3.addWidget(self.appControlWidget, 0, Qt.AlignRight)

        self.horizontalLayout_3.setStretch(1, 5)

        self.verticalLayout.addWidget(self.header, 0, Qt.AlignTop)

        self.appStacks = QStackedWidget(self.centralwidget)
        self.appStacks.setObjectName(u"appStacks")
        self.mainPage = QWidget()
        self.mainPage.setObjectName(u"mainPage")
        self.verticalLayout_3 = QVBoxLayout(self.mainPage)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.mainBody = QWidget(self.mainPage)
        self.mainBody.setObjectName(u"mainBody")
        self.verticalLayout_2 = QVBoxLayout(self.mainBody)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.controlWidget = QWidget(self.mainBody)
        self.controlWidget.setObjectName(u"controlWidget")
        self.verticalLayout_5 = QVBoxLayout(self.controlWidget)
        self.verticalLayout_5.setSpacing(8)  # Aumentado
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(16, 16, 16, 16)  # Aumentado
        self.mediaHandleFrame = QFrame(self.controlWidget)
        self.mediaHandleFrame.setObjectName(u"mediaHandleFrame")
        self.mediaHandleFrame.setFrameShape(QFrame.StyledPanel)
        self.mediaHandleFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.mediaHandleFrame)
        self.horizontalLayout_8.setSpacing(8)  # Aumentado
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(8, 8, 8, 8)  # Aumentado
        self.mediaOpenBtn = QPushButton(self.mediaHandleFrame)
        self.mediaOpenBtn.setObjectName(u"mediaOpenBtn")
        self.mediaOpenBtn.setMinimumSize(QSize(60, 60))  # Aumentado
        icon3 = QIcon()
        icon3.addFile(u":/icons/folder.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaOpenBtn.setIcon(icon3)
        self.mediaOpenBtn.setIconSize(QSize(42, 42))  # Aumentado

        self.horizontalLayout_8.addWidget(self.mediaOpenBtn, 0, Qt.AlignLeft)

        self.mediaFeatFrame = QFrame(self.mediaHandleFrame)
        self.mediaFeatFrame.setObjectName(u"mediaFeatFrame")
        self.mediaFeatFrame.setMaximumSize(QSize(16777215, 16777215))
        self.mediaFeatFrame.setFrameShape(QFrame.StyledPanel)
        self.mediaFeatFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.mediaFeatFrame)
        self.verticalLayout_7.setSpacing(8)  # Aumentado
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(8, 8, 8, 8)  # Aumentado
        self.saveChordsBtn = QPushButton(self.mediaFeatFrame)
        self.saveChordsBtn.setObjectName(u"saveChordsBtn")
        self.saveChordsBtn.setMinimumSize(QSize(48, 48))  # Aumentado
        icon4 = QIcon()
        icon4.addFile(u":/icons/upload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.saveChordsBtn.setIcon(icon4)
        self.saveChordsBtn.setIconSize(QSize(28, 28))  # Aumentado

        self.verticalLayout_7.addWidget(self.saveChordsBtn, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.keyLabel = QLabel(self.mediaFeatFrame)
        self.keyLabel.setObjectName(u"keyLabel")
        self.keyLabel.setAlignment(Qt.AlignCenter)
        # Font para el label de tonalidad
        key_font = QFont("Segoe UI Semibold", 14)
        self.keyLabel.setFont(key_font)

        self.verticalLayout_7.addWidget(self.keyLabel)
        
        self.chordSlider = QSlider(self.mediaFeatFrame)
        self.chordSlider.setObjectName(u"chordSlider")
        self.chordSlider.setMinimumHeight(24)  # Aumentado
        self.chordSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_7.addWidget(self.chordSlider)

        self.horizontalLayout_8.addWidget(self.mediaFeatFrame)

        self.mediaPlayBtn = QPushButton(self.mediaHandleFrame)
        self.mediaPlayBtn.setObjectName(u"mediaPlayBtn")
        self.mediaPlayBtn.setMinimumSize(QSize(60, 60))  # Aumentado
        icon5 = QIcon()
        icon5.addFile(u":/icons/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaPlayBtn.setIcon(icon5)
        self.mediaPlayBtn.setIconSize(QSize(42, 42))  # Aumentado

        self.horizontalLayout_8.addWidget(self.mediaPlayBtn, 0, Qt.AlignRight)

        self.verticalLayout_5.addWidget(self.mediaHandleFrame)

        self.verticalLayout_2.addWidget(self.controlWidget, 0, Qt.AlignTop)

        # Sección de acordes - ZONA PRINCIPAL
        self.chordsWidget = QWidget(self.mainBody)
        self.chordsWidget.setObjectName(u"chordsWidget")
        self.chordsWidget.setMaximumSize(QSize(16777215, 16777215))
        self.chordsWidgetHLayout = QHBoxLayout(self.chordsWidget)
        self.chordsWidgetHLayout.setSpacing(12)  # Aumentado
        self.chordsWidgetHLayout.setObjectName(u"chordsWidgetHLayout")
        self.chordsWidgetHLayout.setContentsMargins(16, 16, 16, 16)  # Aumentado
        
        # Botón seek previous
        self.seekPrevBtn = QPushButton(self.chordsWidget)
        self.seekPrevBtn.setObjectName(u"seekPrevBtn")
        self.seekPrevBtn.setMinimumSize(QSize(36, 36))  # Aumentado
        icon6 = QIcon()
        icon6.addFile(u":/icons/left-arrow-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.seekPrevBtn.setIcon(icon6)
        self.seekPrevBtn.setIconSize(QSize(32, 32))  # Aumentado

        self.chordsWidgetHLayout.addWidget(self.seekPrevBtn, 0, Qt.AlignLeft)

        # Botones de acordes, aumentados de tamaño
        self.prePrevChordBtn = QPushButton(self.chordsWidget)
        self.prePrevChordBtn.setObjectName(u"prePrevChordBtn")
        self.prePrevChordBtn.setMinimumSize(QSize(100, 100))  # Aumentado
        self.prePrevChordBtn.setMaximumSize(QSize(1600, 1600))  # Aumentado
        self.prePrevChordBtn.setFont(self.musical_font)

        self.chordsWidgetHLayout.addWidget(self.prePrevChordBtn, 0, Qt.AlignVCenter)

        self.prevChordBtn = QPushButton(self.chordsWidget)
        self.prevChordBtn.setObjectName(u"prevChordBtn")
        self.prevChordBtn.setMinimumSize(QSize(150, 150))  # Aumentado
        self.prevChordBtn.setMaximumSize(QSize(1600, 1600))  # Aumentado
        # Fuente más grande para los acordes
        prev_chord_font = QFont("Segoe UI", 16)
        self.prevChordBtn.setFont(prev_chord_font)

        self.chordsWidgetHLayout.addWidget(self.prevChordBtn, 0, Qt.AlignVCenter)

        self.currentChordBtn = QPushButton(self.chordsWidget)
        self.currentChordBtn.setObjectName(u"currentChordBtn")
        self.currentChordBtn.setMinimumSize(QSize(200, 200))  # Aumentado
        self.currentChordBtn.setMaximumSize(QSize(1600, 1600))  # Aumentado
        # Fuente más grande para el acorde actual
        current_chord_font = QFont("Segoe UI", 22, QFont.Bold)
        self.currentChordBtn.setFont(current_chord_font)

        self.chordsWidgetHLayout.addWidget(self.currentChordBtn, 0, Qt.AlignVCenter)

        self.nxtChordBtn = QPushButton(self.chordsWidget)
        self.nxtChordBtn.setObjectName(u"nxtChordBtn")
        self.nxtChordBtn.setMinimumSize(QSize(150, 150))  # Aumentado
        self.nxtChordBtn.setMaximumSize(QSize(1600, 1600))  # Aumentado
        self.nxtChordBtn.setFont(prev_chord_font)

        self.chordsWidgetHLayout.addWidget(self.nxtChordBtn, 0, Qt.AlignVCenter)

        self.postNxtChordBtn = QPushButton(self.chordsWidget)
        self.postNxtChordBtn.setObjectName(u"postNxtChordBtn")
        self.postNxtChordBtn.setMinimumSize(QSize(100, 100))  # Aumentado
        self.postNxtChordBtn.setMaximumSize(QSize(1600, 1600))  # Aumentado
        self.postNxtChordBtn.setFont(self.musical_font)

        self.chordsWidgetHLayout.addWidget(self.postNxtChordBtn, 0, Qt.AlignVCenter)

        self.seekNxtBtn = QPushButton(self.chordsWidget)
        self.seekNxtBtn.setObjectName(u"seekNxtBtn")
        self.seekNxtBtn.setMinimumSize(QSize(36, 36))  # Aumentado
        icon7 = QIcon()
        icon7.addFile(u":/icons/right-arrow-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.seekNxtBtn.setIcon(icon7)
        self.seekNxtBtn.setIconSize(QSize(32, 32))  # Aumentado

        self.chordsWidgetHLayout.addWidget(self.seekNxtBtn, 0, Qt.AlignRight)

        self.verticalLayout_2.addWidget(self.chordsWidget)

        # Reproductor de medios
        self.mediaPlayer = QWidget(self.mainBody)
        self.mediaPlayer.setObjectName(u"mediaPlayer")
        self.verticalLayout_4 = QVBoxLayout(self.mediaPlayer)
        self.verticalLayout_4.setSpacing(8)  # Aumentado
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(16, 16, 16, 16)  # Aumentado
        self.mediaProgressFrame = QFrame(self.mediaPlayer)
        self.mediaProgressFrame.setObjectName(u"mediaProgressFrame")
        self.mediaProgressFrame.setFrameShape(QFrame.StyledPanel)
        self.mediaProgressFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.mediaProgressFrame)
        self.horizontalLayout_5.setSpacing(12)  # Aumentado
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.currentPlayedLabel = QLabel(self.mediaProgressFrame)
        self.currentPlayedLabel.setMinimumWidth(64)  # Aumentado
        self.currentPlayedLabel.setObjectName(u"currentPlayedLabel")
        self.currentPlayedLabel.setAlignment(Qt.AlignCenter)
        # Fuente para los indicadores de tiempo
        time_font = QFont("Segoe UI", 12)
        self.currentPlayedLabel.setFont(time_font)

        self.horizontalLayout_5.addWidget(self.currentPlayedLabel)

        self.mediaProgressSlider = SeekSlider(Qt.Horizontal, parent=self.mediaProgressFrame)
        self.mediaProgressSlider.setObjectName(u"mediaProgressSlider")
        self.mediaProgressSlider.setMinimumSize(QSize(400, 24))  # Aumentado
        self.mediaProgressSlider.setOrientation(Qt.Horizontal)
        self.mediaProgressSlider.setCursor(Qt.PointingHandCursor)

        self.horizontalLayout_5.addWidget(self.mediaProgressSlider)

        self.mediaDurationLabel = QLabel(self.mediaProgressFrame)
        self.mediaDurationLabel.setMinimumWidth(64)  # Aumentado
        self.mediaDurationLabel.setObjectName(u"mediaDurationLabel")
        self.mediaDurationLabel.setAlignment(Qt.AlignCenter)
        self.mediaDurationLabel.setFont(time_font)

        self.horizontalLayout_5.addWidget(self.mediaDurationLabel)

        self.verticalLayout_4.addWidget(self.mediaProgressFrame)

        self.mediaInfoFrame = QFrame(self.mediaPlayer)
        self.mediaInfoFrame.setObjectName(u"mediaInfoFrame")
        self.mediaInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.mediaInfoFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.mediaInfoFrame)
        self.horizontalLayout_6.setSpacing(12)  # Aumentado
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.mediaTitleLabel = QLabel(self.mediaInfoFrame)
        self.mediaTitleLabel.setObjectName(u"mediaTitleLabel")
        self.mediaTitleLabel.setMaximumWidth(600)  # Aumentado
        # Fuente para el título del medio
        title_font = QFont("Segoe UI", 12)
        self.mediaTitleLabel.setFont(title_font)

        self.horizontalLayout_6.addWidget(self.mediaTitleLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.mediaMuteBtn = QPushButton(self.mediaInfoFrame)
        self.mediaMuteBtn.setObjectName(u"mediaMuteBtn")
        self.mediaMuteBtn.setMinimumSize(QSize(36, 36))  # Aumentado
        icon8 = QIcon()
        icon8.addFile(u":/icons/volume-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaMuteBtn.setIcon(icon8)
        self.mediaMuteBtn.setIconSize(QSize(24, 24))  # Aumentado

        self.horizontalLayout_6.addWidget(self.mediaMuteBtn, 0, Qt.AlignRight)

        self.volumeSlider = SeekSlider(Qt.Horizontal, parent=self.mediaInfoFrame)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setMinimumSize(QSize(150, 24))  # Aumentado
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setCursor(Qt.PointingHandCursor)

        self.horizontalLayout_6.addWidget(self.volumeSlider, 0, Qt.AlignRight)

        self.verticalLayout_4.addWidget(self.mediaInfoFrame)

        self.verticalLayout_2.addWidget(self.mediaPlayer, 0, Qt.AlignBottom)

        self.verticalLayout_3.addWidget(self.mainBody)

        self.appStacks.addWidget(self.mainPage)
        
        # Página de carga
        self.loadingPage = QWidget()
        self.loadingPage.setObjectName(u"loadingPage")
        self.verticalLayout_6 = QVBoxLayout(self.loadingPage)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget = QWidget(self.loadingPage)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_8 = QVBoxLayout(self.widget)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.loadingGif = QMovie(u":/gif/1479.gif")
        self.loadingGif.setScaledSize(QSize(150, 150))  # Aumentado
        self.label.setMovie(self.loadingGif)

        self.verticalLayout_9.addWidget(self.label)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)
        # Fuente para el texto de carga
        loading_font = QFont("Segoe UI", 14)
        self.label_2.setFont(loading_font)

        self.verticalLayout_9.addWidget(self.label_2)

        self.verticalLayout_8.addWidget(self.frame)
        self.verticalLayout_6.addWidget(self.widget, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        self.appStacks.addWidget(self.loadingPage)

        # Página de error
        self.errPage = QWidget()
        self.errPage.setObjectName(u"errPage")
        self.verticalLayout_10 = QVBoxLayout(self.errPage)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.errWidget = QWidget(self.errPage)
        self.errWidget.setObjectName(u"errWidget")
        self.horizontalLayout_7 = QHBoxLayout(self.errWidget)
        self.horizontalLayout_7.setSpacing(16)  # Aumentado
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.errIconLabel = QLabel(self.errWidget)
        self.errIconLabel.setObjectName(u"errIconLabel")
        self.errIconLabel.setMinimumSize(QSize(100, 100))  # Aumentado
        self.errGif = QMovie(u":/gif/1483 (1).gif")
        self.errGif.setScaledSize(QSize(100, 100))  # Aumentado
        self.errIconLabel.setMovie(self.errGif)

        self.horizontalLayout_7.addWidget(self.errIconLabel)

        self.errLabel = QLabel(self.errWidget)
        self.errLabel.setObjectName(u"errLabel")
        # Fuente para el mensaje de error
        error_font = QFont("Segoe UI", 14)
        self.errLabel.setFont(error_font)

        self.horizontalLayout_7.addWidget(self.errLabel)

        self.verticalLayout_10.addWidget(self.errWidget, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        self.appStacks.addWidget(self.errPage)

        self.verticalLayout.addWidget(self.appStacks)

        # Footer
        self.footer = QWidget(self.centralwidget)
        self.footer.setObjectName(u"footer")
        self.footer.setMinimumHeight(40)  # Aumentado
        self.horizontalLayout = QHBoxLayout(self.footer)
        self.horizontalLayout.setSpacing(8)  # Aumentado
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(16, 8, 16, 8)  # Aumentado
        self.authorLabel = QLabel(self.footer)
        self.authorLabel.setObjectName(u"authorLabel")
        # Fuente para la etiqueta del autor
        author_font = QFont("Segoe UI", 10)
        self.authorLabel.setFont(author_font)

        self.horizontalLayout.addWidget(self.authorLabel)

        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.footerSpacer)

        self.githubBtn = QPushButton(self.footer)
        self.githubBtn.setObjectName(u"githubBtn")
        self.githubBtn.setMaximumSize(QSize(24, 24))  # Aumentado
        icon9 = QIcon()
        icon9.addFile(u":/icons/github.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.githubBtn.setIcon(icon9)
        self.githubBtn.setIconSize(QSize(20, 20))  # Aumentado

        self.horizontalLayout.addWidget(self.githubBtn, 0, Qt.AlignRight)

        self.resizeFrame = QFrame(self.footer)
        self.resizeFrame.setObjectName(u"resizeFrame")
        self.resizeFrame.setMaximumSize(QSize(24, 24))  # Aumentado
        self.horizontalLayout_4 = QHBoxLayout(self.resizeFrame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.resizeLabel = QLabel(self.resizeFrame)
        self.resizeLabel.setObjectName(u"resizeLabel")
        self.resizeLabel.setMinimumSize(QSize(24, 24))  # Aumentado
        self.resizeLabel.setMaximumSize(QSize(24, 24))  # Aumentado
        self.resizeLabel.setPixmap(QPixmap(u":/icons/cil-size-grip.png").scaled(24, 24, Qt.KeepAspectRatio))

        self.horizontalLayout_4.addWidget(self.resizeLabel, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.resizeFrame, 0, Qt.AlignRight|Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.footer, 0, Qt.AlignBottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.appStacks.setCurrentIndex(0)
        self.mediaProgressSlider.setEnabled(False)
        self.mediaPlayBtn.setEnabled(False)
        self.seekNxtBtn.setEnabled(False)
        self.seekPrevBtn.setEnabled(False)
        self.saveChordsBtn.setEnabled(False)
        self.chordSlider.setEnabled(False)
        self.keyLabel.hide()

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ChordFlow - Análisis Armónico", None))
        self.appNameLabel.setText(QCoreApplication.translate("MainWindow", u"  ChordFlow!", None))
#if QT_CONFIG(tooltip)
        self.themeBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Cambiar Tema", None))
#endif // QT_CONFIG(tooltip)
        self.themeBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimizar", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Cerrar", None))
#endif // QT_CONFIG(tooltip)
        self.closeBtn.setText("")
#if QT_CONFIG(tooltip)
        self.mediaOpenBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Abrir Archivo de Audio", None))
#endif // QT_CONFIG(tooltip)
        self.mediaOpenBtn.setText("")
#if QT_CONFIG(tooltip)
        self.saveChordsBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Exportar Acordes como Archivo de Texto", None))
#endif // QT_CONFIG(tooltip)
        self.saveChordsBtn.setText("")
#if QT_CONFIG(tooltip)
        self.keyLabel.setToolTip(QCoreApplication.translate("MainWindow", u"Tonalidad y Tempo", None))
#endif // QT_CONFIG(tooltip)
        self.keyLabel.setText(QCoreApplication.translate("MainWindow", u"", None))
#if QT_CONFIG(tooltip)
        self.mediaPlayBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Reproducir/Pausar", None))
#endif // QT_CONFIG(tooltip)
        self.mediaPlayBtn.setText("")
#if QT_CONFIG(tooltip)
        self.seekPrevBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Retroceder 10s", None))
#endif // QT_CONFIG(tooltip)
        self.seekPrevBtn.setText("")
#if QT_CONFIG(tooltip)
        self.prePrevChordBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Acorde Anterior al Anterior", None))
#endif // QT_CONFIG(tooltip)
        self.prePrevChordBtn.setText(QCoreApplication.translate("MainWindow", u"\U0001F319", None))
#if QT_CONFIG(tooltip)
        self.prevChordBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Acorde Anterior", None))
#endif // QT_CONFIG(tooltip)
        self.prevChordBtn.setText(QCoreApplication.translate("MainWindow", u"\u2600", None))
#if QT_CONFIG(tooltip)
        self.currentChordBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Acorde Actual", None))
#endif // QT_CONFIG(tooltip)
        self.currentChordBtn.setText(QCoreApplication.translate("MainWindow", u"\u2B50", None))
#if QT_CONFIG(tooltip)
        self.nxtChordBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Siguiente Acorde", None))
#endif // QT_CONFIG(tooltip)
        self.nxtChordBtn.setText(QCoreApplication.translate("MainWindow", u"\U0001F319", None))
#if QT_CONFIG(tooltip)
        self.postNxtChordBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Siguiente Después del Siguiente Acorde", None))
#endif // QT_CONFIG(tooltip)
        self.postNxtChordBtn.setText(QCoreApplication.translate("MainWindow", u"\u2600", None))
#if QT_CONFIG(tooltip)
        self.seekNxtBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Avanzar 10s", None))
#endif // QT_CONFIG(tooltip)
        self.seekNxtBtn.setText("")
#if QT_CONFIG(tooltip)
        self.mediaPlayer.setToolTip(QCoreApplication.translate("MainWindow", u"Duración Total", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentPlayedLabel.setToolTip(QCoreApplication.translate("MainWindow", u"Tiempo Actual", None))
#endif // QT_CONFIG(tooltip)
        self.currentPlayedLabel.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
#if QT_CONFIG(tooltip)
        self.mediaProgressSlider.setToolTip(QCoreApplication.translate("MainWindow", u"Buscar aquí", None))
#endif // QT_CONFIG(tooltip)
        self.mediaDurationLabel.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
#if QT_CONFIG(tooltip)
        self.mediaTitleLabel.setToolTip(QCoreApplication.translate("MainWindow", u"Título del Medio", None))
#endif // QT_CONFIG(tooltip)
        self.mediaTitleLabel.setText(QCoreApplication.translate("MainWindow", u"¡Selecciona o Arrastra una Canción!", None))
#if QT_CONFIG(tooltip)
        self.mediaMuteBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Silenciar/Activar Sonido", None))
#endif // QT_CONFIG(tooltip)
        self.mediaMuteBtn.setText("")
#if QT_CONFIG(tooltip)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setToolTip(QCoreApplication.translate("MainWindow", u"Cambiar Volumen", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Analizando Acordes", None))
        self.errIconLabel.setText("")
        self.errLabel.setText(QCoreApplication.translate("MainWindow", u"Error al analizar los acordes", None))
#if QT_CONFIG(tooltip)
        self.authorLabel.setToolTip(QCoreApplication.translate("MainWindow", u"Desarrollador", None))
#endif // QT_CONFIG(tooltip)
        self.authorLabel.setText(QCoreApplication.translate("MainWindow", u"@pavelec", None))
#if QT_CONFIG(tooltip)
        self.githubBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Repositorio de la Aplicación", None))
#endif // QT_CONFIG(tooltip)
        self.githubBtn.setText("")
#if QT_CONFIG(tooltip)
        self.resizeLabel.setToolTip(QCoreApplication.translate("MainWindow", u"", None))
#endif // QT_CONFIG(tooltip)
        self.resizeLabel.setText("")
    # retranslateUi
    
    # Método para cambiar entre temas
    def toggle_theme(self, MainWindow, is_dark=False):
        if is_dark:
            MainWindow.setStyleSheet(pastel_dark_theme)
            icon = QIcon()
            icon.addFile(u":/icons/moon.svg", QSize(), QIcon.Normal, QIcon.Off)
            self.themeBtn.setIcon(icon)
        else:
            MainWindow.setStyleSheet(pastel_light_theme)
            icon = QIcon()
            icon.addFile(u":/icons/sun.svg", QSize(), QIcon.Normal, QIcon.Off)
            self.themeBtn.setIcon(icon)