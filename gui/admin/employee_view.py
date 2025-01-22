from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from database.db_connector import get_connection
from gui.base_window import font
from database.models import Employee
from gui.view import View


class EmployeeView(View):
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

        # filtrowanie po: 'Imię', 'Nazwisko', 'Adres', 'Numer telefonu', 'Email'
        self.filter_name = QLineEdit()
        self.filter_name.setPlaceholderText("Imię")
        filter_layout.addWidget(self.filter_name)
        self.filter_surname = QLineEdit()
        self.filter_surname.setPlaceholderText("Nazwisko")
        filter_layout.addWidget(self.filter_surname)
        self.filter_address = QLineEdit()
        self.filter_address.setPlaceholderText("Adres")
        filter_layout.addWidget(self.filter_address)
        self.filter_phone_number = QLineEdit()
        self.filter_phone_number.setPlaceholderText("Numer telefonu")
        filter_layout.addWidget(self.filter_phone_number)
        self.filter_email = QLineEdit()
        self.filter_email.setPlaceholderText("E-mail")
        filter_layout.addWidget(self.filter_email)

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
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
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
        self.filter_name.clear()
        self.filter_surname.clear()
        self.filter_address.clear()
        self.filter_phone_number.clear()
        self.filter_email.clear()
        self.active_filter = False
        self.display(self.employees)

    def apply_filter(self):
        if not hasattr(self, 'employees'):
            print("Dane nie zostały jeszcze załadowane!")
            return

        filtered_employees = []
        input_name = self.filter_name.text()
        input_surname = self.filter_surname.text()
        input_address = self.filter_address.text()
        input_phone_number = self.filter_phone_number.text()
        input_email = self.filter_email.text()
        is_filter_applied = False

        # filtrowanie
        for employee in self.employees:
            if input_name:
                if input_name.lower() not in employee.first_name.lower():
                    continue
                is_filter_applied = True
            if input_surname:
                if input_surname.lower() not in employee.last_name.lower():
                    continue
                is_filter_applied = True
            if input_address:
                if input_address.lower() not in employee.address.lower():
                    continue
                is_filter_applied = True
            if input_phone_number:
                if input_phone_number.lower() not in employee.phone_number.lower():
                    continue
                is_filter_applied = True
            if input_email:
                if input_email.lower() not in employee.email.lower():
                    continue
                is_filter_applied = True
    
            filtered_employees.append(employee)

        self.active_filter = is_filter_applied
        if not filtered_employees:
            # print("Brak elementów spełniających kryteria filtrowania.")
            self.table.setRowCount(0)
        else:
            self.display(filtered_employees if is_filter_applied else self.employees)
            
    def apply_sort(self):
        sort_key = self.sort_combo.currentText()
        sort_map = {
            "Imię": lambda employee: employee.first_name.lower() if employee.first_name else "",
            "Nazwisko": lambda employee: employee.last_name.lower() if employee.last_name else "",
            "Adres": lambda employee: employee.address.lower() if employee.address else ""
        }

        if self.sort_combo.itemText(0) == "":
            self.sort_combo.removeItem(0)

        if sort_key in sort_map:
            try:
                self.employees.sort(key=sort_map[sort_key], reverse=self.is_sort_descending)

                if self.active_filter:
                    self.apply_filter()
                else:
                    self.display(self.employees)
            except Exception as e:
                print(f"Błąd podczas sortowania: {e}")
        else:
            print(f"Nieprawidłowy klucz sortowania: {sort_key}")

    def create_sort_section(self):
        sort_layout = QHBoxLayout()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["", "Imię", "Nazwisko", "Adres"])
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
            self.employees = Employee.get_all(connection)
            self.display(self.employees)
        except Exception as e:
            print(f"Błąd ładowania pracowników do tabeli: {e}")

    def refresh(self):
        """Odświeża dane w widoku."""
        self.load_to_table()
        
    def display(self, employees):
        self.table.setRowCount(len(employees))
        for row_index, employee in enumerate(employees):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(employee.employee_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(employee.first_name)))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(employee.last_name)))
            self.table.setItem(row_index, 3, QTableWidgetItem(str(employee.address)))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(employee.phone_number)))
            self.table.setItem(row_index, 5, QTableWidgetItem(str(employee.email)))
        self.table.resizeColumnsToContents()

    # --- Metody szczegółowe ---
