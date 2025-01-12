class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.balance = 1500  # Domyślna wartość salda
        self.position = 0  # Start
        self.owned_properties = []
        self.cards = []

    def move(self, steps):
        self.position = (self.position + steps) % 40  # Zakładamy 40 pól na planszy
        return self.position

    def update_balance(self, amount):
        self.balance += amount

    def add_property(self, property_name):
        self.owned_properties.append(property_name)

    def sell_property(self, property_name):
        """Sprzedaje nieruchomość."""
        if property_name in self.owned_properties:
            self.owned_properties.remove(property_name)
            return True
        return False

    def use_card(self, card):
        """Używa karty z listy gracza."""
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def is_bankrupt(self):
        """Sprawdza, czy gracz zbankrutował."""
        return self.balance < 0

    def to_dict(self):
        """Zwraca informacje o graczu jako słownik."""
        return {
            "name": self.name,
            "color": self.color,
            "balance": self.balance,
            "position": self.position,
            "owned_properties": self.owned_properties,
            "cards": self.cards,
        }
