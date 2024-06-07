from dataclasses import dataclass
from typing import List

from app import db
from app.models.text import Text
from app.services.text_services import TextService

text_service = TextService()

@dataclass(init=False, repr=True, eq=True)
class TextHistory(db.Model):
    __tablename__ = "text_histories"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_id: int = db.Column(db.Integer, db.ForeignKey("texts.id"), nullable=False)
    content: str = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def save(self) -> "TextHistory":
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, id: int) -> "TextHistory":
        return cls.query.get(id)

    @classmethod
    def find_by(cls, **kwargs) -> List["TextHistory"]:
        return cls.query.filter_by(**kwargs).all()

    @staticmethod
    def get_versions_of_text(text_id: int) -> List["TextHistory"]:
        # Obtiene todas las versiones de un texto específico.
        return (
            TextHistory.query.filter_by(text_id=text_id)
            .order_by(TextHistory.timestamp.desc())
            .all()
        )

    def change_to_version(self, version_id: int) -> None:
        # Cambia a una versión específica del texto.
        version = TextHistory.find(version_id)
        
        if version:
            text = text_service.find( self.text_id)
            text.content = version.content
            db.session.commit()