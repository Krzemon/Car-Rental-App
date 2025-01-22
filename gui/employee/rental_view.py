from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from database.db_connector import get_connection
from gui.base_window import font
from database.models import Rental
from gui.view import View
from datetime import datetime

class RentalView(View):
    def __init__(self, ):
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

        status_layout = QHBoxLayout()
        self.status_filter_combo = QComboBox()
        self.status_filter_combo.addItems(["Wszystkie", "Wypożyczony", "Zwrócony"])
        status_layout.addWidget(QLabel("Status:", alignment=Qt.AlignmentFlag.AlignLeft))
        status_layout.addWidget(self.status_filter_combo)
        filter_layout.addLayout(status_layout)

        self.filter_name = QLineEdit()
        self.filter_name.setPlaceholderText("Imię lub Nazwisko")
        filter_layout.addWidget(self.filter_name)

        date1_label = QLabel("Data wypożyczenia (YYYY-MM-DD):")
        filter_layout.addWidget(date1_label)
        self.date1_input = QLineEdit()
        self.date1_input.setInputMask("0000-00-00")
        self.date2_input = QLineEdit()
        self.date2_input.setInputMask("0000-00-00")
        date1_layout = QHBoxLayout()
        date1_layout.addWidget(self.date1_input)
        date1_layout.addWidget(self.date2_input)
        filter_layout.addLayout(date1_layout)

        date2_label = QLabel("Data zwrotu (YYYY-MM-DD):")
        filter_layout.addWidget(date2_label)
        self.date3_input = QLineEdit()
        self.date3_input.setInputMask("0000-00-00")
        self.date4_input = QLineEdit()
        self.date4_input.setInputMask("0000-00-00")
        date2_layout = QHBoxLayout()
        date2_layout.addWidget(self.date3_input)
        date2_layout.addWidget(self.date4_input)
        filter_layout.addLayout(date2_layout)

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
        self.table.setColumnCount(7)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels([
            'ID rezerwacji', 'Imię i nazwisko klienta', 'Numer telefonu', 'Samochód', 'Status', 'Data wypożyczenia', 'Data zwrotu'
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
        self.status_filter_combo.setCurrentIndex(0)
        self.filter_name.clear()
        self.date1_input.clear()
        self.date2_input.clear()
        self.date3_input.clear()
        self.date4_input.clear()
        self.active_filter = False
        self.display(self.rentals)

    def apply_filter(self):
        if not hasattr(self, 'rentals'):
            print("Dane nie zostały jeszcze załadowane!")
            return

        filtered_rentals = []
        selected_status = self.status_filter_combo.currentText()
        input_name = self.filter_name.text()
        input_date_1 = self.date1_input.text()
        input_date_2 = self.date2_input.text()
        input_date_3 = self.date3_input.text()
        input_date_4 = self.date4_input.text()
        is_filter_applied = False

        # filtrowanie
        for rental in self.rentals:
            if input_name:
                if input_name.lower() not in rental.first_name.lower():
                    continue
                is_filter_applied = True
            if selected_status != "Wszystkie":
                if rental.rental_status != selected_status:
                    continue
                is_filter_applied = True
            # cos nie działa w formacie daty datetime.strptime() dlatego pass
            if input_date_1 != "__-__-____":
                try:
                    input_date_11 = datetime.strptime(input_date_1, "%Y-%m-%d").date()
                    if rental.created_at < input_date_11:
                        continue
                except ValueError:
                    pass
                is_filter_applied = True
            if input_date_2 != "__-__-____":
                try:
                    input_date_22 = datetime.strptime(input_date_2, "%Y-%m-%d").date()
                    if rental.created_at > input_date_22:
                        continue
                except ValueError:
                    pass
                is_filter_applied = True
            if input_date_3 != "__-__-____":
                try:
                    input_date_33 = datetime.strptime(input_date_3, "%Y-%m-%d").date()
                    if rental.created_at < input_date_33:
                        continue
                except ValueError:
                    pass
                is_filter_applied = True
            if input_date_4 != "__-__-____":
                try:
                    input_date_44 = datetime.strptime(input_date_4, "%Y-%m-%d").date()
                    if rental.created_at > input_date_44:
                        continue
                except ValueError:
                    pass
                is_filter_applied = True

            filtered_rentals.append(rental)

        self.active_filter = is_filter_applied
        if not filtered_rentals:
            # print("Brak elementów spełniających kryteria filtrowania.")
            self.table.setRowCount(0)
        else:
            self.display(filtered_rentals if is_filter_applied else self.rentals)
            
    def apply_sort(self):
        sort_key = self.sort_combo.currentText()
        sort_map = {
            "Data wypożyczenia": lambda rental: rental.rental_date
        }

        if self.sort_combo.itemText(0) == "":
            self.sort_combo.removeItem(0)

        if sort_key in sort_map:
            try:
                self.rentals.sort(key=sort_map[sort_key], reverse=self.is_sort_descending)

                if self.active_filter:
                    self.apply_filter()
                else:
                    self.display(self.rentals)
            except Exception as e:
                print(f"Błąd podczas sortowania: {e}")
        else:
            print(f"Nieprawidłowy klucz sortowania: {sort_key}")

    def create_sort_section(self):
        sort_layout = QHBoxLayout()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["", "Data wypożyczenia"])
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
            self.rentals = Rental.get_all(connection)
            self.display(self.rentals)
        except Exception as e:
            print(f"Błąd ładowania wypożyczeń do tabeli: {e}")

    def refresh(self):
        """Odświeża dane w widoku."""
        self.load_to_table()
        
    def display(self, rentals):
        self.table.setRowCount(len(rentals))
        for row_index, rental in enumerate(rentals):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(rental.rental_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(rental.customer_name))
            self.table.setItem(row_index, 2, QTableWidgetItem(rental.phone_number))
            self.table.setItem(row_index, 3, QTableWidgetItem(rental.car_name))
            self.table.setItem(row_index, 4, QTableWidgetItem(rental.rental_status))
            self.table.setItem(row_index, 5, QTableWidgetItem(str(rental.rental_date)))
            self.table.setItem(row_index, 6, QTableWidgetItem(str(rental.return_date) if rental.return_date else ''))

        self.table.resizeColumnsToContents()

    # --- Metody szczegółowe ---
