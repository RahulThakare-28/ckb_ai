"""
db_connections_test.py
===================

it is uesd to test the db_connections.py module

"""
from db_service.db_connections import MongoDBConnection



def test_mongodb_connection():
    """
    Basic test for MongoDBConnection lifecycle.
    """

    db_connection = MongoDBConnection()

    # Get database (handles connection internally)
    db = db_connection.get_database()

    if db is not None :
        print("✅ MongoDB connected successfully")

        try:
            # Test real operation
            collections = db.list_collection_names()
            print(f"📂 Collections: {collections}")

        except Exception as e:
            print(f"❌ Error while accessing DB: {e}")

    else:
        print("❌ MongoDB connection failed")

    # Close connection
    if db_connection.close_connection():
        print("🔒 MongoDB connection closed successfully")
    else:
        print("⚠️ No connection to close or failed to close")


if __name__ == "__main__":
    test_mongodb_connection()

    