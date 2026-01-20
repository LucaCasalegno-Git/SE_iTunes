from dataclasses import dataclass


@dataclass
class Album:
    id: int
    title: str
    artist_id: int
    durata: float

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.id}- {self.title}, {self.artist_id}: {self.durata}"

    def __repr__(self):
        return f"{self.id}- {self.title}, {self.artist_id}: {self.durata}"