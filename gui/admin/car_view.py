from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem, QComboBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from database.db_connector import get_connection
from gui.base_window import font
from database.models import Car
from gui.view import View

import json
import os

class CarView(View):
    def __init__(self):
        super().__init__()

        self.is_sort_descending = False
        self.active_filter = False
        self.color_translations = self.load_color_translations()
        self.fuel_translations = self.load_fuel_translations()
        self.type_translations = self.load_type_translations()

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

        color_layout = QHBoxLayout()
        self.color_filter_combo = QComboBox()
        self.color_filter_combo.addItems(["Wszystkie", "Czerwony", "Niebieski", "Czarny", "Biały", "Szary", "Pomarańczowy", "Beżowy", "Zielony", "Żółty"])
        color_layout.addWidget(QLabel("Kolor:", alignment=Qt.AlignmentFlag.AlignLeft))
        color_layout.addWidget(self.color_filter_combo)
        filter_layout.addLayout(color_layout)

        # Filtrowanie po rodzaju paliwa
        fuel_layout = QHBoxLayout()
        self.fuel_filter_combo = QComboBox()
        self.fuel_filter_combo.addItems(["Wszystkie", "Benzyna", "Diesel", "Elektryczny", "Hybryda"])
        fuel_layout.addWidget(QLabel("Rodzaj paliwa:", alignment=Qt.AlignmentFlag.AlignLeft))
        fuel_layout.addWidget(self.fuel_filter_combo)
        filter_layout.addLayout(fuel_layout)

        # Filtrowanie po liczbie miejsc
        seats_layout = QHBoxLayout()
        self.seats_filter_combo = QComboBox()
        self.seats_filter_combo.addItems(["Wszystkie", '2', '4', '5', '7', '9'])
        seats_layout.addWidget(QLabel("Liczba miejsc: ", alignment=Qt.AlignmentFlag.AlignLeft))
        seats_layout.addWidget(self.seats_filter_combo)
        filter_layout.addLayout(seats_layout)

        # Filtrowanie po typie pojazdu
        type_layout = QHBoxLayout()
        self.type_filter_combo = QComboBox()
        self.type_filter_combo.addItems(["Wszystkie", "Coupe", "Hatchback", "Kabriolet", "Kombi", "Sedan", "SUV", "Van"])
        type_layout.addWidget(QLabel("Typ pojazdu: ", alignment=Qt.AlignmentFlag.AlignLeft))
        type_layout.addWidget(self.type_filter_combo)
        filter_layout.addLayout(type_layout)

        year_layout_a = QHBoxLayout()
        year_layout_b = QHBoxLayout()

        self.year_min = QSlider(Qt.Orientation.Horizontal)
        self.year_min.setRange(2000, 2025)
        self.year_min.setValue(2000)
        self.year_min.setTracking(True)  # Aby suwak reagował na ruch od razu
        self.year_min.valueChanged.connect(self.update_year_min_label)  # Po zmianie wartości

        self.year_max = QSlider(Qt.Orientation.Horizontal)
        self.year_max.setRange(2000, 2025)
        self.year_max.setValue(2025)
        self.year_max.setTracking(True)
        self.year_max.valueChanged.connect(self.update_year_max_label)

        self.year_min_label = QLabel(str(self.year_min.value()))
        self.year_max_label = QLabel(str(self.year_max.value()))

        self.year_min.valueChanged.connect(self.sync_min) # min < max
        self.year_max.valueChanged.connect(self.sync_max)

        filter_layout.addWidget(QLabel("Rok produkcji:"))
        year_layout_a.addWidget(QLabel("od:"))
        year_layout_a.addWidget(self.year_min)
        year_layout_a.addWidget(self.year_min_label)
        year_layout_b.addWidget(QLabel("do:"))
        year_layout_b.addWidget(self.year_max)
        year_layout_b.addWidget(self.year_max_label)

        filter_layout.addLayout(year_layout_a)
        filter_layout.addLayout(year_layout_b)

        price_layout = QHBoxLayout()
        self.price_min = QSpinBox()
        self.price_min.setRange(0, 100)
        self.price_max = QSpinBox()
        self.price_max.setRange(0, 100)
        self.price_min.setValue(20)
        self.price_max.setValue(90)
        price_layout.addWidget(QLabel("Cena od:"))
        price_layout.addWidget(self.price_min)
        price_layout.addWidget(QLabel("do:"))
        price_layout.addWidget(self.price_max)
        filter_layout.addLayout(price_layout)

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
        self.table.setColumnCount(13)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels([
            'ID samochodu', 'Marka', 'Model', 'Rok', 'Nr rejestracyjny', 'Dzienna stawka',
            'VIN', 'Status', 'Rodzaj paliwa', 'Status ubezpieczenia', 'Liczba miejsc', 'Kolor', 'Typ pojazdu'
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

    def load_to_table(self):
        try:
            connection = get_connection()
            self.cars = Car.get_all(connection)  # Pobieramy wszystkie samochody
            self.display(self.cars)  # Wyświetlamy pełną listę w tabeli
        except Exception as e:
            print(f"Błąd ładowania samochodów do tabeli: {e}")

    def refresh(self):
        """Odświeża dane w widoku."""
        self.load_to_table()

    def reset_filter(self):
        self.color_filter_combo.setCurrentIndex(0)
        self.fuel_filter_combo.setCurrentIndex(0)
        self.seats_filter_combo.setCurrentIndex(0)
        self.type_filter_combo.setCurrentIndex(0)
        self.year_min.setValue(2000)
        self.year_max.setValue(2025)
        self.price_min.setValue(0)
        self.price_max.setValue(100)
        self.active_filter = False
        self.display(self.cars)

    def apply_filter(self):
        if not hasattr(self, 'cars'):  # Sprawdzenie, czy dane są załadowane
            print("Dane nie zostały jeszcze załadowane!")
            return

        filtered_cars = []
        selected_color = self.color_filter_combo.currentText()
        selected_fuel = self.fuel_filter_combo.currentText()
        selected_seats = self.seats_filter_combo.currentText()
        selected_type = self.type_filter_combo.currentText()
        
        is_filter_applied = False

        for car in self.cars:
            if selected_color != "Wszystkie":
                english_color = {v: k for k, v in self.color_translations.items()}.get(selected_color)
                if english_color is None:
                    print(f"Błąd: nie znaleziono tłumaczenia dla {selected_color}")
                    continue
                if car.color != english_color:
                    continue
                is_filter_applied = True

            if selected_fuel != "Wszystkie":
                english_fuel = {v: k for k, v in self.fuel_translations.items()}.get(selected_fuel)
                if english_fuel is None:
                    print(f"Błąd: nie znaleziono tłumaczenia dla {selected_fuel}")
                    continue
                if car.fuel_type != english_fuel:
                    continue
                is_filter_applied = True

            if selected_type != "Wszystkie":
                english_type = {v: k for k, v in self.type_translations.items()}.get(selected_type)
                if english_type is None:
                    print(f"Błąd: nie znaleziono tłumaczenia dla {selected_type}")
                    continue
                if car.type != english_type:
                    continue
                is_filter_applied = True

            if selected_seats != "Wszystkie":
                if car.seat_count != int(selected_seats):
                    continue
                is_filter_applied = True

            if not (self.year_min.value() <= car.year <= self.year_max.value()):
                continue
            else:
                is_filter_applied = True

            if not (self.price_min.value() <= car.daily_rate <= self.price_max.value()):
                continue
            else:
                is_filter_applied = True
            filtered_cars.append(car)

        self.active_filter = is_filter_applied
        if not filtered_cars:
            print("Brak elementów spełniających kryteria filtrowania.")
            self.table.setRowCount(0)  # Wyczyść tabelę
        else:
            self.display(filtered_cars if is_filter_applied else self.cars)

    def apply_sort(self):
        sort_key = self.sort_combo.currentText()
        sort_map = {
            "Marka": lambda car: car.make.lower() if car.make else "",
            "Model": lambda car: car.model.lower() if car.model else "",
            "Rok": lambda car: car.year,
            "Dzienna stawka": lambda car: car.daily_rate 
        }

        if self.sort_combo.itemText(0) == "":
            self.sort_combo.removeItem(0)

        if sort_key in sort_map:
            try:
                self.cars.sort(key=sort_map[sort_key], reverse=self.is_sort_descending)

                if self.active_filter:
                    self.apply_filter()
                else:
                    self.display(self.cars)
            except Exception as e:
                print(f"Błąd podczas sortowania: {e}")
        else:
            print(f"Nieprawidłowy klucz sortowania: {sort_key}")

    def create_sort_section(self):
        sort_layout = QHBoxLayout()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["", "Marka", "Model", "Rok", "Dzienna stawka"])
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

    def display(self, cars):
        self.table.setRowCount(len(cars))
        for row_index, car in enumerate(cars):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(car.car_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(car.make)))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(car.model)))
            self.table.setItem(row_index, 3, QTableWidgetItem(str(car.year)))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(car.license_plate)))
            self.table.setItem(row_index, 5, QTableWidgetItem(str(car.daily_rate)))
            self.table.setItem(row_index, 6, QTableWidgetItem(str(car.vin)))
            self.table.setItem(row_index, 7, QTableWidgetItem(str(car.status)))
            self.table.setItem(row_index, 8, QTableWidgetItem(str(car.fuel_type)))
            self.table.setItem(row_index, 9, QTableWidgetItem(str(car.insurance_status)))
            self.table.setItem(row_index, 10, QTableWidgetItem(str(car.seat_count)))
            self.table.setItem(row_index, 11, QTableWidgetItem(str(car.color)))
            self.table.setItem(row_index, 12, QTableWidgetItem(str(car.type)))
        self.table.resizeColumnsToContents()

    # --- Metody szczegółowe ---

    def update_year_min_label(self):
        self.year_min_label.setText(str(self.year_min.value()))

    def update_year_max_label(self):
        self.year_max_label.setText(str(self.year_max.value()))

    def sync_min(self):
        """Synchronizowanie suwaków 'od' i 'do', aby 'do' nie mogło być mniejsze od 'od'."""
        if self.year_min.value() > self.year_max.value():
            self.year_max.setValue(self.year_min.value())

    def sync_max(self):
        """Synchronizowanie suwaków 'od' i 'do', aby 'do' nie mogło być mniejsze od 'od'."""
        if self.year_max.value() < self.year_min.value():
            self.year_min.setValue(self.year_max.value())

    def load_color_translations(self):
        """Wczytuje tłumaczenia kolorów z pliku JSON."""
        try:
            colors_file = os.path.join("config", "translated", "colors.json")
            with open(colors_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Nie znaleziono pliku colors.json.")
            return {}
        except json.JSONDecodeError:
            print("Błąd podczas parsowania pliku colors.json.")
            return {}
        
    def load_fuel_translations(self):
        """Wczytuje tłumaczenia rodzajów paliwa z pliku JSON."""
        try:
            fuel_file = os.path.join("config", "translated", "fuel_type.json")
            with open(fuel_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Nie znaleziono pliku fuel_type.json.")
            return {}
        except json.JSONDecodeError:
            print("Błąd podczas parsowania pliku fuel_type.json.")
            return {}

    def load_type_translations(self):
        """Wczytuje tłumaczenia typow pojazdow z pliku JSON."""
        try:
            type_file = os.path.join("config", "translated", "type.json")
            with open(type_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Nie znaleziono pliku type.json.")
            return {}
        except json.JSONDecodeError:
            print("Błąd podczas parsowania pliku type.json.")
            return {}