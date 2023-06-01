from models.base_model import BaseModel
from repositories.base_repository import BaseRepository
from typing import List, TypeVar, Generic

#Enforce that any Class passed to this service must implement our BaseModel
#This is necessary to generically work with properties found on our BaseModel such as completed & deleted whilst ensuring type safety.

T = TypeVar('T', bound=BaseModel)

class BaseService(Generic[T]):

    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository
        self.model_class = repository.model_class

    def get_by_id(self, id) -> T | None:
        return self.repository.get_by_id(id)
    
    def get_all(self) -> List[T | None]:
        return self.repository.get_all()
    
    def get_count(self) -> int:
        return self.repository.get_count_from_table()

    def filter_deleted(self, bool: bool, items: list[T]) -> list[T | None]:
        return list(filter(lambda t: t.deleted == bool, items))
    
    def filter_complete(self, bool: bool, items: list[T]) -> list[T | None]:
        return list(filter(lambda t: t.completed == bool, items))
    
    def check_if_deleted(self, item: T) -> bool:
        return item.deleted
    
    def check_if_completed(self, item: T) -> bool:
        return item.completed