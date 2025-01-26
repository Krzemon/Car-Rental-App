from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox

from database.db_connector import get_connection
import json
import os

class ChangeStatusWindow(QWidget):
    """Okno zmiany statusu płatności."""
    def __init__(self):
        super().__init__()

        self.payment_translations = self.load_payment_translations()

        self.setWindowTitle("Zmień Status Samochodu")
        self.setGeometry(150, 150, 400, 300)

        self.form_layout = QFormLayout()
        self.id_input = QLineEdit()
        self.form_layout.addRow("ID Płatności:", self.id_input)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Opłacone", "Nie opłacone"])
        self.form_layout.addRow("Status:", self.status_combo)
        self.change_button = QPushButton("Zmień Status")
        self.change_button.clicked.connect(self.change_status_in_db)
        self.form_layout.addWidget(self.change_button)
        self.setLayout(self.form_layout)

    def change_status_in_db(self):
        """Zmienia status płatności w bazie danych."""
        payment_id = self.id_input.text()
        new_status = self.status_combo.currentText()

        reverse_payment_translations = {v: k for k, v in self.payment_translations.items()}
        english_status = reverse_payment_translations.get(new_status)

        if not payment_id:
            QMessageBox.warning(self, "Błąd", "Wprowadź ID płatności.")
            return
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "UPDATE projekt_bd1.payments SET status = %s WHERE payment_id = %s",
                (english_status, payment_id)
            )
            if cursor.rowcount > 0:
                connection.commit()
                QMessageBox.information(self, "Sukces", f"Status płatności o ID {payment_id} został zmieniony na '{english_status}'.")
            else:
                QMessageBox.warning(self, "Błąd", f"Płatność o ID {payment_id} nie istnieje.")
        except Exception as e:
            print(f"Błąd podczas zmiany statusu: {e}")
            QMessageBox.warning(self, "Błąd", "Wystąpił błąd podczas zmiany statusu.")

        self.close()

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