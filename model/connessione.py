from dataclasses import dataclass

@dataclass
class Connessione:
    id_rifugio1 : int
    id_rifugio2 : int
    weight: float

def __eq__(self, other):
    return self.id_rifugio1 == other.id_rifugio1 and self.id_rifugio2 == other.id_rifugio2

def __str__(self):
    return f"id_rifugio1: {self.id_rifugio1}, id_rifugio2: {self.id_rifugio2}, weight: {self.weight}"