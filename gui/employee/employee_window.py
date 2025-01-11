from gui.base_window import BaseWindow

class EmployeeWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        # Dodatkowe elementy i logika specyficzna dla CustomerWindow
        self.setWindowTitle("Employee Window")
        
    def employee_specific_method(self):
        print("This is a method specific to the customer window.")
