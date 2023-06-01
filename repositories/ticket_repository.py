from datetime import datetime
from models.ticket_model import TicketModel
from repositories.base_repository import BaseRepository
from repositories.database_connection import DatabaseConnection
from repositories.seed_database_tickets import generate_dummy_tickets

class TicketRepository(BaseRepository):
    def __init__(self, db_conn: DatabaseConnection, table_name: str):
        super().__init__(db_conn, table_name, TicketModel)
        self.create_table()
        if (self.get_count_from_table() == 0):
            self.seed_database()
            
    def create_table(self):
        self.db.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                created_date TEXT,
                updated_date TEXT,
                completed BOOLEAN,
                deleted BOOLEAN,
                priority INTEGER,
                ticket_type TEXT,
                title TEXT,
                description TEXT,
                initial_estimate REAL,
                remaining_time REAL,
                logged_time REAL
            )
        ''')
        self.db.connection.commit()

    def seed_database(self): 
            for record in generate_dummy_tickets():
                self.add_to_db(record)

    #Should be generic enough to use in BaseRepo with an ORM, but SQL implementation is too specific to be generic.
    def add_to_db(self, ticket: TicketModel) -> TicketModel:
        """
        Adds a new ticket to the database.

        Args:
            ticket (TicketModel): The ticket object to be added.

        Returns:
            TicketModel: The newly created ticket object.

        Raises:
            Any database-related exceptions that may occur during execution.

        Notes:
            This functionality would typically be found on my base repository.
            Without an ORM the implementation of these repetitive methods needs to be specific.
        """

        #TODO: In theory, this could be refactored with string interpolation at run time, reading the names of the keys of TicketModel
        #to generate script in a generic manner

        query = f"""
        INSERT INTO {self.table_name} (
            created_date, updated_date, completed, deleted, 
            priority, ticket_type, title, description, 
            initial_estimate, remaining_time, logged_time
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """
        values = (
            ticket.created_date, ticket.updated_date, int(ticket.completed), int(ticket.deleted), 
            ticket.priority, ticket.ticket_type.value, ticket.title, ticket.description, 
            ticket.initial_estimate, ticket.remaining_time, ticket.logged_time
        )

        self.db.cursor.execute(query, values)
        self.db.connection.commit()

        # Return the newly created ticket
        return self.get_by_id(self.db.cursor.lastrowid)
    
    def update_record(self, id: int, updated_record: TicketModel, date: datetime):
        query = f"""
        UPDATE {self.table_name} 
        SET updated_date = ?, 
            priority = ?, 
            ticket_type = ?, 
            title = ?, 
            description = ?
        WHERE id = ?
        """

        values = (
            date,
            updated_record.priority,
            updated_record.ticket_type,
            updated_record.title,
            updated_record.description,
            id
        )

        self.db.cursor.execute(query, values)
        self.db.connection.commit()

        return self.get_by_id(id)
    
    def delete_record(self, id: int, date: datetime) -> TicketModel:
        query = f"""
        UPDATE {self.table_name}
        SET deleted = ?, updated_date = ?
        WHERE id = ?
        """

        self.db.cursor.execute(query, (1, date, id))
        self.db.connection.commit()
        return self.get_by_id(id)
    
    def complete_record(self, id: int, date: datetime) -> TicketModel:
        query = f"""
        UPDATE {self.table_name}
        SET completed = ?, updated_date = ?
        WHERE id = ?
        """

        self.db.cursor.execute(query, (1, date, id))
        self.db.connection.commit()
        return self.get_by_id(id)

    def log_time(self, id: int, remaining_time: float, logged_time: float, date: datetime) -> TicketModel:
        query = f"""
        UPDATE {self.table_name}
        SET remaining_time = ?, logged_time = ?, updated_date = ?
        WHERE id = ?
        """

        self.db.cursor.execute(query, (remaining_time, logged_time, date, id))
        self.db.connection.commit()
        return self.get_by_id(id)




