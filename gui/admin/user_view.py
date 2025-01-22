from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from database.db_connector import get_connection
from gui.base_window import font
from database.models import User
from gui.view import View
from datetime import datetime

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

        # filtrowanie po: 'Rola','Status', 'Email', 'Data utworzenia'
        role_layout = QHBoxLayout()
        self.role_filter_combo = QComboBox()
        self.role_filter_combo.addItems(["Wszystkie", "admin", "customer", "employee"])
        role_layout.addWidget(QLabel("Rola:", alignment=Qt.AlignmentFlag.AlignLeft))
        role_layout.addWidget(self.role_filter_combo)
        filter_layout.addLayout(role_layout)
        
        status_layout = QHBoxLayout()
        self.status_filter_combo = QComboBox()
        self.status_filter_combo.addItems(["Wszystkie", "active", "blocked", "deleted"])
        status_layout.addWidget(QLabel("Status:", alignment=Qt.AlignmentFlag.AlignLeft))
        status_layout.addWidget(self.status_filter_combo)
        filter_layout.addLayout(status_layout)

        self.filter_email = QLineEdit()
        self.filter_email.setPlaceholderText("E-mail")
        filter_layout.addWidget(self.filter_email)

        date_label = QLabel("Data utworzenia konta (YYYY-MM-DD):")
        filter_layout.addWidget(date_label)
        self.date1_input = QLineEdit()
        self.date1_input.setInputMask("0000-00-00")
        self.date2_input = QLineEdit()
        self.date2_input.setInputMask("0000-00-00")
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date1_input)
        date_layout.addWidget(self.date2_input)
        filter_layout.addLayout(date_layout)

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
        self.table.setColumnCount(5)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels([
            'ID użytkownika', 'Email', 'Rola', 'Status', 'Data utworzenia'
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
        self.role_filter_combo.setCurrentIndex(0)
        self.status_filter_combo.setCurrentIndex(0)
        self.filter_email.clear()
        self.date1_input.clear()
        self.date2_input.clear()
        self.active_filter = False
        self.display(self.users)

    def apply_filter(self):
        if not hasattr(self, 'users'):
            print("Dane nie zostały jeszcze załadowane!")
            return

        filtered_users = []
        selected_role = self.role_filter_combo.currentText()
        selected_status = self.status_filter_combo.currentText()
        input_email = self.filter_email.text()
        input_date_1 = self.date1_input.text()
        input_date_2 = self.date2_input.text()
        is_filter_applied = False

        # filtrowanie
        for user in self.users:
            if selected_role != "Wszystkie":
                if user.role != selected_role:
                    continue
                is_filter_applied = True
            if selected_status != "Wszystkie":
                if user.status != selected_status:
                    continue
                is_filter_applied = True
            if input_email:
                if input_email.lower() not in user.email.lower():
                    continue
                is_filter_applied = True

            # cos nie działa w formacie daty datetime.strptime() dlatego pass
            if input_date_1 != "__-__-____":
                try:
                    input_date_11 = datetime.strptime(input_date_1, "%Y-%m-%d").date()
                    if user.created_at < input_date_11:
                        continue
                except ValueError:
                    pass
                is_filter_applied = True
                
            if input_date_2 != "__-__-____":
                try:
                    input_date_22 = datetime.strptime(input_date_2, "%Y-%m-%d").date()
                    if user.created_at > input_date_22:
                        continue
                except ValueError:
                    pass
                is_filter_applied = True

            filtered_users.append(user)

        self.active_filter = is_filter_applied
        if not filtered_users:
            # print("Brak elementów spełniających kryteria filtrowania.")
            self.table.setRowCount(0)
        else:
            self.display(filtered_users if is_filter_applied else self.users)

    def apply_sort(self):
        sort_key = self.sort_combo.currentText()
        sort_map = {
            "Rola": lambda user: user.role.lower() if user.role else "",
            "Status": lambda user: user.status.lower() if user.status else "",
            "Email": lambda user: user.email.lower() if user.email else "",
            "Data utworzenia": lambda user: user.created_at
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
        self.sort_combo.addItems(["", "Rola", "Status", "Email", "Data utworzenia"])
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

    def refresh(self):
        """Odświeża dane w widoku."""
        self.load_to_table()
        
    def display(self, users):
        self.table.setRowCount(len(users))
        for row_index, user in enumerate(users):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(user.user_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(user.email)))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(user.role)))
            self.table.setItem(row_index, 3, QTableWidgetItem(str(user.status)))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(user.created_at)))
        self.table.resizeColumnsToContents()

    # --- Metody szczegółowe ---
