from PyQt6.QtWidgets import QTabWidget

from gui.base_window import BaseWindow
from gui.employee.car_view import CarView
from gui.employee.rental_view import RentalView
from gui.employee.payment_view import PaymentView

class EmployeeWindow(BaseWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user

        self.title_label.setText("Panel Pracownika")
        self.tabs = QTabWidget(self)

        self.car_view = CarView()
        self.rental_view = RentalView()
        self.payment_view = PaymentView()   

        self.cars_widget = self.car_view.create()
        self.rental_widget = self.rental_view.create()
        self.payment_widget = self.payment_view.create()

        self.tabs.addTab(self.cars_widget, "Samochody")
        self.tabs.addTab(self.rental_widget, "Wypożyczenia")
        self.tabs.addTab(self.payment_widget, "Płatności")

        # Po zmianie zakładki wywołujemy metodę on_tab_changed
        self.tabs.currentChanged.connect(self.on_tab_changed)

        # Dodanie zakładek do layoutu klasy bazowej
        self.layout.addWidget(self.tabs)  # Używamy layoutu z klasy BaseWindow
        self.setLayout(self.layout)  # Zachowujemy layout z klasy BaseWindow

    def on_tab_changed(self, index):
        """Slot wywoływany przy zmianie zakładki."""
        if index == 0:
            self.car_view.refresh()
        elif index == 1:
            self.rental_view.refresh()
        elif index == 2:
            self.payment_view.refresh()

    def refresh_tab1(self):
        """Odświeża dane w Zakładce 1."""
        print("Dane dla Zakładki 1 zostały odświeżone.")

    def refresh_tab2(self):
        """Odświeża dane w Zakładce 2."""
        print("Dane dla Zakładki 2 zostały odświeżone.")
