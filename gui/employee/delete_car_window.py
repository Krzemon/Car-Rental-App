from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox

from database.db_connector import get_connection

class DeleteCarWindow(QWidget):
    """Okno usuwania samochodu z bazy danych."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Usuń Samochód")
        self.setGeometry(150, 150, 400, 200)

        self.form_layout = QFormLayout()
        self.id_input = QLineEdit()
        self.form_layout.addRow("ID Samochodu:", self.id_input)
        self.remove_button = QPushButton("Usuń Samochód")
        self.remove_button.clicked.connect(self.remove_car_from_db)
        self.form_layout.addWidget(self.remove_button)
        self.setLayout(self.form_layout)

    def remove_car_from_db(self):
        """Usuwa samochód z bazy danych."""
        car_id = self.id_input.text()
        if not car_id:
            QMessageBox.warning(self, "Błąd", "Wprowadź ID samochodu.")
            return
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM projekt_bd1.cars WHERE car_id = %s", (car_id,))
            if cursor.rowcount > 0:
                connection.commit()  # Zatwierdzenie transakcji
                QMessageBox.information(self, "Sukces", f"Samochód o ID {car_id} został usunięty.")
            else:
                QMessageBox.warning(self, "Błąd", f"Samochód o ID {car_id} nie istnieje.")
        except Exception as e:
            print(f"Błąd podczas usuwania samochodu: {e}")
            QMessageBox.warning(self, "Błąd", "Wystąpił błąd podczas usuwania samochodu.")
            
        self.close()