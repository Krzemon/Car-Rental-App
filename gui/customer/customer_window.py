from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CustomerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Welcome, Customer!"))
        self.setLayout(self.layout)