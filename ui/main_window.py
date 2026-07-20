from ui.themes import DARK_THEME, LIGHT_THEME

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QMessageBox,
    QFrame
)

from script.database import Database


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.db = Database()

        self.dark = True

        self.setWindowTitle("UPTAC Cutoff Bot")
        self.resize(1200, 750)

        self.build_ui()

        self.setStyleSheet(DARK_THEME)

        self.load_colleges()

        # Signals
        self.search_box.textChanged.connect(self.filter_colleges)

        self.college_combo.currentTextChanged.connect(self.load_quotas)
        self.quota_combo.currentTextChanged.connect(self.load_categories)
        self.category_combo.currentTextChanged.connect(self.load_genders)

        self.show_button.clicked.connect(self.show_cutoff)

        self.theme_button.clicked.connect(self.change_theme)

    # ===================================
    # UI
    # ===================================

    def build_ui(self):

        main = QVBoxLayout(self)

        main.setContentsMargins(20,20,20,20)
        main.setSpacing(20)

        # ---------------- HEADER ----------------

        header = QFrame()
        header.setObjectName("Header")

        header_layout = QHBoxLayout(header)

        title = QLabel("🎓 UPTAC CUTOFF BOT")
        title.setObjectName("Title")

        header_layout.addWidget(title)

        header_layout.addStretch()

        self.theme_button = QPushButton("🌙")
        self.theme_button.setFixedSize(45,45)

        header_layout.addWidget(self.theme_button)

        main.addWidget(header)

        # ---------------- CARD ----------------

        card = QFrame()
        card.setObjectName("Card")

        grid = QGridLayout(card)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search College..."
        )

        self.college_combo = QComboBox()

        self.quota_combo = QComboBox()

        self.category_combo = QComboBox()

        self.gender_combo = QComboBox()

        self.show_button = QPushButton("🔍 Show Cutoff")

        grid.addWidget(QLabel("Search"),0,0)
        grid.addWidget(self.search_box,0,1)

        grid.addWidget(QLabel("College"),1,0)
        grid.addWidget(self.college_combo,1,1)

        grid.addWidget(QLabel("Quota"),2,0)
        grid.addWidget(self.quota_combo,2,1)

        grid.addWidget(QLabel("Category"),3,0)
        grid.addWidget(self.category_combo,3,1)

        grid.addWidget(QLabel("Seat Gender"),4,0)
        grid.addWidget(self.gender_combo,4,1)

        grid.addWidget(self.show_button,5,0,1,2)

        main.addWidget(card)

        # ---------------- TABLE ----------------

        self.table = QTableWidget()

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        main.addWidget(self.table)

    # ===================================
    # THEME
    # ===================================

    def change_theme(self):

        if self.dark:

            self.setStyleSheet(LIGHT_THEME)

            self.dark = False

            self.theme_button.setText("☀")

        else:

            self.setStyleSheet(DARK_THEME)

            self.dark = True

            self.theme_button.setText("🌙")

                # ===================================
    # LOAD COLLEGES
    # ===================================

    def load_colleges(self):

        self.college_combo.clear()

        colleges = self.db.get_colleges()

        self.college_combo.addItems(colleges)

        if colleges:
            self.load_quotas()

    # ===================================
    # SEARCH COLLEGE
    # ===================================

    def filter_colleges(self):

        text = self.search_box.text().strip()

        colleges = self.db.search_colleges(text)

        self.college_combo.blockSignals(True)

        self.college_combo.clear()

        self.college_combo.addItems(colleges)

        self.college_combo.blockSignals(False)

        if colleges:
            self.college_combo.setCurrentIndex(0)
            self.load_quotas()

    # ===================================
    # LOAD QUOTA
    # ===================================

    def load_quotas(self):

        self.quota_combo.clear()
        self.category_combo.clear()
        self.gender_combo.clear()

        quotas = self.db.get_quotas(
            self.college_combo.currentText()
        )

        self.quota_combo.addItems(quotas)

        if quotas:
            self.quota_combo.setCurrentIndex(0)
            self.load_categories()

    # ===================================
    # LOAD CATEGORY
    # ===================================

    def load_categories(self):

        self.category_combo.clear()
        self.gender_combo.clear()

        categories = self.db.get_categories(
            self.college_combo.currentText(),
            self.quota_combo.currentText()
        )

        self.category_combo.addItems(categories)

        if categories:
            self.category_combo.setCurrentIndex(0)
            self.load_genders()

    # ===================================
    # LOAD GENDER
    # ===================================

    def load_genders(self):

        self.gender_combo.clear()

        genders = self.db.get_genders(
            self.college_combo.currentText(),
            self.quota_combo.currentText(),
            self.category_combo.currentText()
        )

        self.gender_combo.addItems(genders)

    # ===================================
    # SHOW CUTOFF
    # ===================================

    def show_cutoff(self):

        df = self.db.search(

            self.college_combo.currentText(),

            self.quota_combo.currentText(),

            self.category_combo.currentText(),

            self.gender_combo.currentText()

        )

        self.table.clear()

        if df.empty:

            self.table.setRowCount(0)
            self.table.setColumnCount(0)

            QMessageBox.information(
                self,
                "No Data",
                "No cutoff found."
            )

            return

        self.table.setRowCount(len(df))

        self.table.setColumnCount(len(df.columns))

        self.table.setHorizontalHeaderLabels(df.columns.tolist())

        for row in range(len(df)):
            for col in range(len(df.columns)):

                item = QTableWidgetItem(
                    str(df.iloc[row, col])
                )

                item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(
                    row,
                    col,
                    item
                )

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        self.table.setAlternatingRowColors(True)