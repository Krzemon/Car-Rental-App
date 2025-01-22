from abc import ABC, abstractmethod

class View(ABC):
    """Klasa bazowa dla widoków zakładek."""
    
    @abstractmethod
    def create(self):
        """Tworzy widok."""
        pass
    
    @abstractmethod
    def load_to_table(self):
        """Ładuje dane do tabeli."""
        pass

    @abstractmethod
    def refresh(self):
        """Odświeża dane w widoku."""
        pass
    
    @abstractmethod
    def reset_filter(self):
        """Resetuje wartości filtrów."""
        pass

    @abstractmethod
    def apply_filter(self):
        """Zastosuj filtr do danych."""
        pass

    @abstractmethod
    def apply_sort(self):
        """Sortuje dane w tabeli."""
        pass

    @abstractmethod
    def create_sort_section(self):
        """Tworzy sekcję sortowania."""
        pass

    @abstractmethod
    def toggle_sort_order(self):
        """Zmienia kierunek sortowania (rosnąco/malejąco)."""
        pass

    @abstractmethod
    def display(self, cars):
        """Wyświetla dane w tabeli."""
        pass