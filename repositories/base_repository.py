from typing import List
from repositories.database_connection import DatabaseConnection
from typing import Type, TypeVar, Generic

T = TypeVar('T')

class BaseRepository(Generic[T]):

    def __init__(self, db_connection: DatabaseConnection, table_name: str, model_class: Type[T]):
        self.db = db_connection
        self.table_name = table_name
        self.model_class = model_class
        
    def get_by_id(self, id: int) -> T:
        self.db.cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = ?', (id,))
        result = self.db.cursor.fetchone()
        return self.model_class(*result) if result else None
    
    def get_all(self) -> List[T]:
        self.db.cursor.execute(f'SELECT * FROM {self.table_name}')
        return [self.model_class(*row) for row in self.db.cursor.fetchall()]
    
    def get_count_from_table(self):
        self.db.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return self.db.cursor.fetchone()[0]
    
    
        

