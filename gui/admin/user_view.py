from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QStatusBar, QTabWidget, QPushButton, QSpinBox, QTableWidget, QCheckBox, QTableWidgetItem, QComboBox, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer

from database.db_connector import get_connection
from gui.base_window import font
from database.models import User
from gui.view import View

import json
import os

class UserView(View):
    def __init__(self):
        super().__init__()

        self.is_sort_descending = False
        self.active_filter = False

    def create(self):
        widget = QWidget()
        layout = QVBoxLayout()
        Hlayout = QHBoxLayout()
        filter_layout = QVBoxLayout()
        
        filter_layout.setContentsMargins(0, 0, 0, 0)  # Usuwamy marginesy
        right_widget = QWidget()  # Widget, który będzie kontenerem layoutu
        right_widget.setLayout(filter_layout)
        right_widget.setFixedWidth(300) # Stała szerokość

        filter_label = QLabel("Filtrowanie:", alignment=Qt.AlignmentFlag.AlignLeft)
        filter_label.setFont(font)
        filter_layout.addWidget(filter_label)


        # color_layout = QHBoxLayout()
        # self.color_filter_combo = QComboBox()
        # self.color_filter_combo.addItems(["Wszystkie", "Czerwony", "Niebieski", "Czarny", "Biały", "Szary", "Pomarańczowy", "Beżowy", "Zielony", "Żółty"])
        # color_layout.addWidget(QLabel("Kolor:", alignment=Qt.AlignmentFlag.AlignLeft))
        # color_layout.addWidget(self.color_filter_combo)
        # filter_layout.addLayout(color_layout)


        # zrow wpisywane filtry i sprawdzane na bieżąco???


        spacer_for_filter = QSpacerItem(50, 10, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        filter_layout.addItem(spacer_for_filter)

        reset_filter_button = QPushButton("Resetuj filtry")
        reset_filter_button.clicked.connect(self.reset_filter)
        filter_layout.addWidget(reset_filter_button)

        filter_button = QPushButton("Zastosuj filtry")
        filter_button.clicked.connect(self.apply_filter)
        filter_layout.addWidget(filter_button)
    
        # Sortowanie
        sort_layout = self.create_sort_section()
        layout.addLayout(sort_layout)

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'ID pracownika', 'Imię', 'Nazwisko', 'Adres', 'Numer telefonu', 'Email'
        ])
        self.load_to_table()

        left_layout = QVBoxLayout()

        left_layout.addWidget(self.table)
        Hlayout.addLayout(left_layout)

        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.Shape.VLine)
        vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
        Hlayout.addWidget(vertical_line)

        Hlayout.addWidget(right_widget)
        layout.addLayout(Hlayout)

        widget.setLayout(layout)
        return widget

    def reset_filter(self):
        self.display(self.users)

    def apply_filter(self):
        if not hasattr(self, 'users'):
            print("Dane nie zostały jeszcze załadowane!")
            return

        filtered_users = []
        is_filter_applied = False

        # filtrowanie
        for user in self.users:
            # if selected_color != "Wszystkie":
            filtered_users.append(user)

        self.active_filter = is_filter_applied
        if not filtered_users:
            print("Brak elementów spełniających kryteria filtrowania.")
            self.table.setRowCount(0)
        else:
            self.display(filtered_users if is_filter_applied else self.users)
            
    def apply_sort(self):
        sort_key = self.sort_combo.currentText()
        sort_map = {
            "Imię": lambda user: user.first_name.lower() if user.first_name else "",
            "Nazwisko": lambda user: user.last_name.lower() if user.last_name else "",
            "Adres": lambda user: user.address.lower() if user.address else ""
        }

        if self.sort_combo.itemText(0) == "":
            self.sort_combo.removeItem(0)

        if sort_key in sort_map:
            try:
                self.users.sort(key=sort_map[sort_key], reverse=self.is_sort_descending)

                if self.active_filter:
                    self.apply_filter()
                else:
                    self.display(self.users)
            except Exception as e:
                print(f"Błąd podczas sortowania: {e}")
        else:
            print(f"Nieprawidłowy klucz sortowania: {sort_key}")

    def create_sort_section(self):
        sort_layout = QHBoxLayout()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["", "Rola", "Status"])
        self.sort_combo.currentIndexChanged.connect(self.apply_sort)

        sorter_label = QLabel("Sortuj według:", alignment=Qt.AlignmentFlag.AlignLeft)
        sorter_label.setFont(font)
        sort_layout.addWidget(sorter_label)
        sort_layout.addWidget(self.sort_combo, alignment=Qt.AlignmentFlag.AlignLeft)

        sort_order_button = QPushButton()
        sort_order_button.setIcon(QIcon("resources/images/sort.png"))
        sort_order_button.setIconSize(QSize(25, 25))
        sort_order_button.setToolTip("Odwróć kolejność sortowania")
        sort_order_button.setFixedSize(30, 30)
        sort_order_button.clicked.connect(self.toggle_sort_order)
        sort_layout.addWidget(sort_order_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sort_layout.addItem(spacer)
        return sort_layout

    def toggle_sort_order(self):
        self.is_sort_descending = not self.is_sort_descending
        self.apply_sort()

    def load_to_table(self):
        try:
            connection = get_connection()
            self.users = User.get_all(connection)
            self.display(self.users)
        except Exception as e:
            print(f"Błąd ładowania użytkowników do tabeli: {e}")

    def display(self, users):
        self.table.setRowCount(len(users))
        for row_index, user in enumerate(users):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(user.user_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(user.email)))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(user.role)))
        self.table.resizeColumnsToContents()

    # --- Metody szczegółowe ---
