from typing import List

from app.models.text import Text
from app.repositories.text_repository import TextRepository
from app.services.security import SecurityManager, WerkzeugSecurity

repository = TextRepository()

class TextService:

    """ Clase que se encarga de CRUD de usuarios """
    def __init__(self) -> None:
        self.__security = SecurityManager(WerkzeugSecurity())

    def save(self, text: Text) -> Text:
        return repository.save(text)
    
    def update(self, text: Text, id: int) -> Text:
        return repository.update(text, id)
    
    def delete(self, text: Text) -> None:
        repository.delete(text)
    
    def all(self) -> List[Text]:
        return repository.all()
    
    def find(self, id: int) -> Text:
        return repository.find(id)
    