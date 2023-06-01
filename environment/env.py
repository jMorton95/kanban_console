"""
Typically we would want to use a .env (dotenv) file to store our environment variables, with our secrets
hidden away from the rest of the application. However since we're making a simple console application,
we won't have any cloud, server, OS or even containerisation available to us, so I'm going to use
magic strings in this module to replicate a .env or secrets management platform.
"""

DB_CONNECTION = "kanban_db.sqlite"

DB_TICKET_STRING = "tickets"

DB_ADM_USER = "very_cool_user"

DB_ADM_PASS = "very_encrypted_password123!"



