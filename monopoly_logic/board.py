class Board:
    def __init__(self):
        self.fields = [
            {"name": "Start", "type": "special", "price": None, "owner": None, "field_ID": 1},  # 0
            {"name": "Ulica Konopacka", "type": "property", "price": 60, "owner": None, "field_ID": 2},  # 1
            {"name": "Kasa Społeczna", "type": "special", "price": None, "owner": None, "field_ID": 12},  # 2
            {"name": "Ulica Stalowa", "type": "property", "price": 60, "owner": None, "field_ID": 2},  # 3
            {"name": "Podatek Dochodowy", "type": "tax", "price": 200, "owner": None, "field_ID": 14},  # 4
            {"name": "Dworzec Zachodni", "type": "railroad", "price": 200, "owner": None, "field_ID": 10},  # 5
            {"name": "Ulica Radzymińska", "type": "property", "price": 100, "owner": None, "field_ID": 3},  # 6
            {"name": "Szansa", "type": "special", "price": None, "owner": None, "field_ID": 13},  # 7
            {"name": "Ulica Jagiellońska", "type": "property", "price": 100, "owner": None, "field_ID": 3},  # 8
            {"name": "Ulica Targowa", "type": "property", "price": 120, "owner": None, "field_ID": 3},  # 9
            {"name": "Więzienie", "type": "special", "price": None, "owner": None, "field_ID": 15},  # 10
            {"name": "Ulica Płowiecka", "type": "property", "price": 140, "owner": None, "field_ID": 4},  # 11
            {"name": "Elektrownia", "type": "utility", "price": 150, "owner": None, "field_ID": 11},  # 12
            {"name": "Ulica Marsa", "type": "property", "price": 140, "owner": None, "field_ID": 4},  # 13
            {"name": "Ulica Grochowska", "type": "property", "price": 160, "owner": None, "field_ID": 4},  # 14
            {"name": "Dworzec Gdański", "type": "railroad", "price": 200, "owner": None, "field_ID": 10},  # 15
            {"name": "Ulica Obozowa", "type": "property", "price": 180, "owner": None, "field_ID": 5},  # 16
            {"name": "Kasa Społeczna", "type": "special", "price": None, "owner": None, "field_ID": 12},  # 17
            {"name": "Ulica Górczewska", "type": "property", "price": 180, "owner": None, "field_ID": 5},  # 18
            {"name": "Ulica Wolska", "type": "property", "price": 200, "owner": None, "field_ID": 5},  # 19
            {"name": "Parking", "type": "special", "price": None, "owner": None, "field_ID": 16},  # 20
            {"name": "Ulica Mickiewicza", "type": "property", "price": 220, "owner": None, "field_ID": 6},  # 21
            {"name": "Szansa", "type": "special", "price": None, "owner": None, "field_ID": 13},  # 22
            {"name": "Ulica Słowackiego", "type": "property", "price": 220, "owner": None, "field_ID": 6},  # 23
            {"name": "Plac Wilsona", "type": "property", "price": 240, "owner": None, "field_ID": 6},  # 24
            {"name": "Dworzec Wschodni", "type": "railroad", "price": 200, "owner": None, "field_ID": 10},  # 25
            {"name": "Ulica Świętokrzyska", "type": "property", "price": 260, "owner": None, "field_ID": 7},  # 26
            {"name": "Krakowskie Przedmieście", "type": "property", "price": 260, "owner": None, "field_ID": 7},  # 27
            {"name": "Wodociągi", "type": "utility", "price": 150, "owner": None, "field_ID": 11},  # 28
            {"name": "Nowy Świat", "type": "property", "price": 280, "owner": None, "field_ID": 7},  # 29
            {"name": "Idź do Więzienia", "type": "special", "price": None, "owner": None, "field_ID": 17},  # 30
            {"name": "Plac Trzech Krzyży", "type": "property", "price": 300, "owner": None, "field_ID": 8},  # 31
            {"name": "Ulica Marszałkowska", "type": "property", "price": 300, "owner": None, "field_ID": 8},  # 32
            {"name": "Kasa Społeczna", "type": "special", "price": None, "owner": None, "field_ID": 12},  # 33
            {"name": "Aleje Jerozolimskie", "type": "property", "price": 320, "owner": None, "field_ID": 8},  # 34
            {"name": "Dworzec Centralny", "type": "railroad", "price": 200, "owner": None, "field_ID": 10},  # 35
            {"name": "Szansa", "type": "special", "price": None, "owner": None, "field_ID": 13},  # 36
            {"name": "Ulica Belwederska", "type": "property", "price": 350, "owner": None, "field_ID": 9},  # 37
            {"name": "Podatek Dochodowy", "type": "tax", "price": 100, "owner": None, "field_ID": 14},  # 38
            {"name": "Aleje Ujazdowskie", "type": "property", "price": 400, "owner": None, "field_ID": 9},  # 39
        ]

    def get_fields(self):
        return self.fields

    def get_field_by_position(self, position):
        return self.fields[position % len(self.fields)]  # Użyj modulo na wypadek przekroczenia liczby pól

    def get_owner(self, position):
        """Zwraca właściciela pola na podstawie pozycji."""
        return self.fields[position]["owner"]
