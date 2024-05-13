from dataclasses import dataclass
from typing import List

from cryptography.fernet import Fernet

from app import db
from app.models.text import Text


@dataclass(init=False, repr=True, eq=True)
class Encriptador(db.Model):
    __tablename__ = "encriptador"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content : str = db.Column(db.String(120), nullable=False)
    encoded_content: bytes = db.Column(db.LargeBinary, nullable=False)

    def save(self) -> "Encriptador":
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def encrypt_content(self):
        key = Fernet.generate_key()
        f = Fernet(key)
        self.encoded_content = f.encrypt(self.content.encode('utf-8'))

    

    @classmethod
    def find(cls, id: int) -> "Encriptador":
        return cls.query.get(id)

    @classmethod
    def find_by(cls, **kwargs) -> List["Encriptador"]:
        return cls.find_by(**kwargs)
