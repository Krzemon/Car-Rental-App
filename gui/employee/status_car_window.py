from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox

from database.db_connector import get_connection

class StatusCarWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zmień status ubezpieczenia samochodu")
        self.setGeometry(150, 150, 400, 200)

        self.form_layout = QFormLayout()
        self.id_input = QLineEdit()
        self.form_layout.addRow("ID Samochodu:", self.id_input)

        self.insurance_status_combo = QComboBox()
        self.insurance_status_combo.addItems(["insured", "uninsured", "expired"])
        self.form_layout.addRow("Status ubezpieczenia:", self.insurance_status_combo)

        self.change_button = QPushButton("Zmień status")
        self.change_button.clicked.connect(self.change_status_in_db)
        self.form_layout.addWidget(self.change_button)
        self.setLayout(self.form_layout)

    def change_status_in_db(self):
        car_id = self.id_input.text()
        new_status = self.insurance_status_combo.currentText()

        if not car_id:
            QMessageBox.warning(self, "Błąd", "Wprowadź ID samochodu.")
            return

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "UPDATE projekt_bd1.cars SET insurance_status = %s WHERE car_id = %s",
                (new_status, car_id)
            )
            if cursor.rowcount > 0:
                connection.commit()
                QMessageBox.information(self, "Sukces", f"Status ubezpieczenia dla samochodu o ID {car_id} został zmieniony na '{new_status}'.")
            else:
                QMessageBox.warning(self, "Błąd", f"Samochód o ID {car_id} nie istnieje.")
        except Exception as e:
            print(f"Błąd podczas zmiany statusu ubezpieczenia: {e}")
            QMessageBox.warning(self, "Błąd", "Wystąpił błąd podczas zmiany statusu ubezpieczenia.")

        self.close()