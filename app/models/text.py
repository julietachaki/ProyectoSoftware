# Importa el decorador dataclass desde el módulo dataclasses
from dataclasses import dataclass, field
from typing import List

# Importa la instancia db desde el módulo app, que parece ser un objeto de SQLAlchemy
from app import db


# Definimos una clase llamada Text utilizando el decorador dataclass
@dataclass(init=False, repr=True, eq=True)
class Text(db.Model):  # Hereda de db.Model, lo que indica que es un modelo de base de datos
    __tablename__ = "texts"  # Nombre de la tabla en la base de datos
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Columna de clave primaria
    content : str = db.Column(db.String(5255), nullable=True)
    length: int = db.Column(db.Integer, nullable=False)  # columna que indica el tamaño del texto
    language: str = db.Column(db.String(120), nullable=False)  # columna que indica el idioma del texto
    # Define la relación con TextHistory y User
    histories = db.relationship("TextHistory", backref="text", lazy=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def change_content(self, new_content: str) -> None:
        # Cambia el contenido del texto y guarda la versión anterior en TextHistory.
        #! ESTO NO SE HACE
        from app.models.text_history import \
            TextHistory  # Importa dentro de la función o método

        old_content = self.content
        self.content = new_content
        history = TextHistory(text_id=self.id, content=old_content)
        history.save()