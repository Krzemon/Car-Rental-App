from gui.base_window import BaseWindow

# blokowanie komorek w tabeli
# self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

class EmployeeWindow(BaseWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        # Dodatkowe elementy i logika specyficzna dla CustomerWindow
        self.setWindowTitle("Employee Window")
        
    def employee_specific_method(self):
        print("This is a method specific to the customer window.")
