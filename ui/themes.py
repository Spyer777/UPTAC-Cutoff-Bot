DARK_THEME = """
QWidget{
    background:#1E1E1E;
    color:white;
    font-family:Segoe UI;
    font-size:11pt;
}

QLabel{
    font-weight:bold;
}

QComboBox,QLineEdit{
    background:#2D2D30;
    border:2px solid #3C3C3C;
    border-radius:8px;
    padding:6px;
    color:white;
}

QComboBox:hover,
QLineEdit:hover{
    border:2px solid #4A90E2;
}

QPushButton{
    background:#0A84FF;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px;
    font-weight:bold;
}

QPushButton:hover{
    background:#0066CC;
}

QPushButton:pressed{
    background:#0052A3;
}

QTableWidget{
    background:#2D2D30;
    border:none;
    gridline-color:#555;
    alternate-background-color:#252526;
}

QHeaderView::section{
    background:#0A84FF;
    color:white;
    padding:8px;
    border:none;
    font-weight:bold;
}

QScrollBar:vertical{
    background:#1E1E1E;
    width:12px;
}

QScrollBar::handle:vertical{
    background:#666;
    border-radius:6px;
}
"""



LIGHT_THEME = """
QWidget{
    background:white;
    color:black;
    font-family:Segoe UI;
    font-size:11pt;
}

QLabel{
    font-weight:bold;
}

QComboBox,QLineEdit{
    background:white;
    border:2px solid #C8C8C8;
    border-radius:8px;
    padding:6px;
}

QComboBox:hover,
QLineEdit:hover{
    border:2px solid #1976D2;
}

QPushButton{
    background:#1976D2;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px;
    font-weight:bold;
}

QPushButton:hover{
    background:#1565C0;
}

QPushButton:pressed{
    background:#0D47A1;
}

QTableWidget{
    background:white;
    alternate-background-color:#F5F5F5;
    gridline-color:#D0D0D0;
}

QHeaderView::section{
    background:#1976D2;
    color:white;
    padding:8px;
    border:none;
    font-weight:bold;
}
"""