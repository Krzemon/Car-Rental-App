# from PyQt6.QtWidgets import QApplication
# from gui.main_window import MainWindow

# def test_admin_view():
#     app = QApplication([])
#     main_window = MainWindow("Administrator")
#     assert main_window.windowTitle() == "Car Rental System - Administrator View"
#     # Sprawdź, czy przycisk "Manage Users" jest obecny
#     assert any(widget.text() == "Manage Users" for widget in main_window.findChildren(QPushButton))

# def test_worker_view():
#     app = QApplication([])
#     main_window = MainWindow("Worker")
#     assert main_window.windowTitle() == "Car Rental System - Worker View"
#     # Sprawdź, czy przycisk "Manage Rentals" jest obecny
#     assert any(widget.text() == "Manage Rentals" for widget in main_window.findChildren(QPushButton))
