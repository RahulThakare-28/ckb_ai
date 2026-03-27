"""
db_connection.py
=================

This module is responsible for establishing a connection to MongoDB using
environment variables. It provides a reusable and loosely coupled interface
to obtain a database instance for performing CRUD operations in other modules.

Environment Variables Required:
- MONGO_URI: MongoDB connection string (local or remote)
- MONGO_DB_NAME: Name of the database to connect to
"""

import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class MongoDBConnection:
    """
    MongoDBConnection handles the creation and management of a MongoDB client.

    This class encapsulates all logic related to database connectivity,
    ensuring loose coupling so other modules can use the database instance
    without worrying about connection details.
    """

    def __init__(self):
        """
        Initializes the MongoDBConnection instance by reading environment variables.
        """
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("MONGO_DB_NAME")
        self.client = None
        self.db = None

    def connect(self):
        """
        Establishes a connection to MongoDB.

        Returns:
            pymongo.database.Database: Database instance if connection is successful.
            None: If connection fails.

        Raises:
            ValueError: If required environment variables are missing.
        """
        try:
            if not self.mongo_uri or not self.db_name:
                raise ValueError("MONGO_URI or MONGO_DB_NAME is not set in .env")

            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]

            # Optional: ping to verify connection
            self.client.admin.command("ping")

            return self.db

        except (PyMongoError, ValueError) as e:
            print(f"[DB CONNECTION ERROR]: {e}")
            return None

    def get_database(self):
        """
        Returns the database instance. If not connected, it attempts to connect first.

        Returns:
            pymongo.database.Database: Database instance.
            None: If connection fails.
        """
        if self.db is None:
            return self.connect()
        return self.db

    def close_connection(self):
        """
        Closes the MongoDB client connection.

        Returns:
            bool: True if closed successfully, False otherwise.
        """
        try:
            if self.client:
                self.client.close()
                return True
            return False
        except PyMongoError as e:
            print(f"[DB CLOSE ERROR]: {e}")
            return False