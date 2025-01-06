from gui.base_window import BaseWindow

class CustomerWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        # Dodatkowe elementy i logika specyficzna dla CustomerWindow
        self.setWindowTitle("Customer Window")
        
    def customer_specific_method(self):
        print("This is a method specific to the customer window.")
