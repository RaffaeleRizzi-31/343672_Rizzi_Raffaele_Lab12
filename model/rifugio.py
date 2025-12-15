from dataclasses import dataclass

@dataclass
class Rifugio:
    id : int
    nome : str
    localita : str
    altitudine : int
    capienza : str
    aperto : int

    def __str__(self):
        return f"[{self.id}] {self.nome} ({self.localita})"

    def __hash__(self):
        return hash(self.id)