from dataclasses import dataclass

from app import db  # Importa la instancia db desde el módulo app

from .text_history import TextHistory


@dataclass(init=False, repr=True, eq=True)
class Texto(db.Model):
    __tablename__ = "text"  # Nombre de la tabla en la base de datos
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content: str = db.Column(db.String(255), nullable=False)
    length: int = db.Column(db.Integer, nullable=False)
    language: str = db.Column(db.String(50), nullable=False)

    # Definición de la relación con la tabla 'text_history' (historial de texto)
    history_id = db.Column(db.Integer, db.ForeignKey("text_history.id"))
    history = db.relationship("TextHistory", back_populates="texts")

    def check_length(self, new_content: str) -> bool:
        """Check if the length of the new content is within the specified limit."""
        return len(new_content) <= self.length

    def encrypt_text(self):
        """Encrypt the content of the text."""
        # Implement encryption logic here
        pass