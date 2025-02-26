# -*- coding: utf-8 -*-
"""
Módulo de temas para DeChord
Contiene los temas originales y los nuevos temas pasteles
"""

# Tema claro con colores pasteles
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

# Tema oscuro con colores pasteles
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

# Los temas originales para mantener compatibilidad
light_theme = """
QWidget {
    background-color: white;
    color: black;
    font-family: Arial;
    font-size: 11pt;
}
QLabel {
    color: black;
}
QPushButton {
    background-color: #EEE;
    color: black;
    border-radius: 5px;
    padding: 4px;
    border: none;
}
QPushButton:hover {
    background-color: #DDD;
}
QPushButton:pressed {
    background-color: #AAA;
}
QSlider::groove:horizontal {
    border-radius: 2px;
    height: 4px;
    background-color: #DDD;
}
QSlider::handle:horizontal {
    background-color: #AAA;
    border-radius: 7px;
    width: 14px;
    margin: -5px 0;
}
QSlider::handle:horizontal:hover {
    background-color: #777;
}
#header, #footer {
    background-color: #EEE;
}
#mainBody {
    background-color: white;
}
"""

dark_theme = """
QWidget {
    background-color: #333;
    color: white;
    font-family: Arial;
    font-size: 11pt;
}
QLabel {
    color: white;
}
QPushButton {
    background-color: #555;
    color: white;
    border-radius: 5px;
    padding: 4px;
    border: none;
}
QPushButton:hover {
    background-color: #666;
}
QPushButton:pressed {
    background-color: #888;
}
QSlider::groove:horizontal {
    border-radius: 2px;
    height: 4px;
    background-color: #555;
}
QSlider::handle:horizontal {
    background-color: #888;
    border-radius: 7px;
    width: 14px;
    margin: -5px 0;
}
QSlider::handle:horizontal:hover {
    background-color: #AAA;
}
#header, #footer {
    background-color: #222;
}
#mainBody {
    background-color: #333;
}
"""