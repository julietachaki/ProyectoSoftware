# Importa el decorador dataclass desde el módulo dataclasses
from dataclasses import dataclass
from typing import List

# from app.models.text_history import TextHistory
from cryptography.fernet import Fernet

# Importa la instancia db desde el módulo app, que parece ser un objeto de SQLAlchemy
from app import db
from app.models.text import Text


# Definimos una clase llamada Text utilizando el decorador dataclass
@dataclass(init=False, repr=True, eq=True)
class Encriptador(db.Model):  # Hereda de db.Model, lo que indica que es un modelo de base de datos
    __tablename__ = "encriptador"  # Nombre de la tabla en la base de datos
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Columna de clave primaria
    key : str = db.Column(db.String(120), nullable=False)  # Columna para el texto
    content = str = db.Column(db.String(120), nullable=False)  # type: ignore
    
    def __init__(self, text_content ):
        self.content = text_content

    def save(self) -> "Encriptador":
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, id: int) -> "Encriptador":
        return cls.query.get(id)

    @classmethod
    def find_by(cls, **kwargs) -> List["Encriptador"]:
        return cls.query.filter_by(**kwargs).all()
    def generate_key(self):
        self.key= Fernet.generate_key()

    # def encrypt_content(self):
    #     f = Fernet(key)
    #     encrypted_content = f.encrypt(self.content.encode())
    #     self.content = encrypted_content.decode()

