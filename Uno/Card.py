class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    
    def __str__(self):
        return f'{self.color.name} {self.value.name}'
    
    def __repr__(self):
        return str(self)