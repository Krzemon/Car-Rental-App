from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class WorkerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Worker Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Welcome, Worker!"))
        self.setLayout(self.layout)