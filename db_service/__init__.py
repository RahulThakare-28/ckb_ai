"""
db_service
==========

This subpackage provides database service functionality for the application.

It includes modules and utilities to manage database connections and perform
operations such as creating, reading, updating, and deleting records.

The package abstracts underlying database interactions, enabling other parts
of the application to work with the database in a consistent and efficient way.
"""

from .db_connections import MongoDBConnection

__all__ = ["MongoDBConnection"]