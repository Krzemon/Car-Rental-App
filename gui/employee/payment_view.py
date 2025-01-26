from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from database.db_connector import get_connection
from gui.base_window import font
from database.models import Payment
from gui.view import View
from gui.employee.change_status_window import ChangeStatusWindow

import json
import os

class PaymentView(View):
    """Klasa reprezentująca widok płatności."""
    def __init__(self):
        super().__init__()
        self.is_sort_descending = False
        self.active_filter = False
        self.payment_translations = self.load_payment_translations()

    def create(self):
        """Tworzy widok płatności."""
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
        self.status_filter_combo.addItems(["Wszystkie", "Opłacone", "Nie opłacone"])
        status_layout.addWidget(QLabel("Status:", alignment=Qt.AlignmentFlag.AlignLeft))
        status_layout.addWidget(self.status_filter_combo)
        filter_layout.addLayout(status_layout)

        self.change_status_button = QPushButton("Zmień Status Samochodu")
        self.change_status_button.clicked.connect(self.open_change_status_window)
        filter_layout.addWidget(self.change_status_button)


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
            'ID płatności', 'ID rezerwacji', 'Data płatności', 'Kwota', 'Status'
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
    
    def open_change_status_window(self):
        """Otwiera okno zmiany statusu płatności."""
        self.change_status_window = ChangeStatusWindow()
        self.change_status_window.show()

    def load_to_table(self):
        """Ładuje dane do tabeli."""
        try:
            connection = get_connection()
            self.payments = Payment.get_all(connection)
            self.display(self.payments)
        except Exception as e:
            print(f"Błąd ładowania płatności do tabeli: {e}")

    def refresh(self):
        """Odświeża dane w widoku."""
        self.load_to_table()
        
    def reset_filter(self):
        """Resetuje filtry."""
        self.status_filter_combo.setCurrentIndex(0)
        self.active_filter = False
        self.display(self.payments)

    def apply_filter(self):
        """Filtruje dane w tabeli."""
        if not hasattr(self, 'payments'):  # Sprawdzenie, czy dane są załadowane
            print("Dane nie zostały jeszcze załadowane!")
            return

        filtered_payments = []
        selected_status = self.status_filter_combo.currentText()
        is_filter_applied = False

        for payment in self.payments:
            if selected_status != "Wszystkie":
                english_paid = {v: k for k, v in self.payment_translations.items()}.get(selected_status)
                if english_paid is None:
                    print(f"Błąd: nie znaleziono tłumaczenia dla {selected_status}")
                    continue
                if payment.status != english_paid:
                    continue
                is_filter_applied = True

            filtered_payments.append(payment)

        self.active_filter = is_filter_applied
        if not filtered_payments:
            print("Brak elementów spełniających kryteria filtrowania.")
            self.table.setRowCount(0)  # Wyczyść tabelę
        else:
            self.display(filtered_payments if is_filter_applied else self.payments)

    def apply_sort(self):
        """Sortuje dane w tabeli."""
        sort_key = self.sort_combo.currentText()
        sort_map = {
            "Status": lambda payment: payment.status
        }

        if self.sort_combo.itemText(0) == "":
            self.sort_combo.removeItem(0)

        if sort_key in sort_map:
            try:
                self.payments.sort(key=sort_map[sort_key], reverse=self.is_sort_descending)

                if self.active_filter:
                    self.apply_filter()
                else:
                    self.display(self.payments)
            except Exception as e:
                print(f"Błąd podczas sortowania: {e}")
        else:
            print(f"Nieprawidłowy klucz sortowania: {sort_key}")

    def create_sort_section(self):
        """Tworzy sekcję sortowania."""
        sort_layout = QHBoxLayout()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["", "Status"])
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
        """Odwraca kolejność sortowania."""
        self.is_sort_descending = not self.is_sort_descending
        self.apply_sort()

    def display(self, payments):
        """Wyświetla płatności w tabeli."""
        self.table.setRowCount(len(payments))
        for row_index, payment in enumerate(payments):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(payment.payment_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(payment.rental_id)))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(payment.payment_date)))
            self.table.setItem(row_index, 3, QTableWidgetItem(str(payment.amount)))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(payment.status)))
        self.table.resizeColumnsToContents()

    # --- Metody szczegółowe ---
    def load_payment_translations(self):
        """Wczytuje tłumaczenia platnosci z pliku JSON."""
        try:
            type_file = os.path.join("config", "translated", "paid.json")
            with open(type_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Nie znaleziono pliku type.json.")
            return {}
        except json.JSONDecodeError:
            print("Błąd podczas parsowania pliku type.json.")
            return {}