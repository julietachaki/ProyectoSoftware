from typing import List, Type

from app import db
from app.models.text import Text


class TextRepository:

    def save(self, text: Text ) -> Text :
        db.session.add(text)
        db.session.commit()
        return text
    def update(self,text:Text,id:int)-> Text:
        entity = self.find(id)
        entity.content = text.content
        db.session.add(entity)
        db.session.commit()
        return entity
    def delete(self, text: Text) -> None:
        db.session.delete(text)
        db.session.commit()

    def all(self) -> List[Text]:
        texts = db.session.query(Text).all()
        return texts
    
    def find(self, id: int) -> Text:
        if id is None or id == 0:
            return None
        try:
            return db.session.query(Text).filter(Text.id == id).one()
        except:
            return None
        
