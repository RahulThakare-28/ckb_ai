"""
Test Module: db_to_doc_test.py

Purpose:
    Test dynamic MongoDB → Document conversion with error handling.
"""

from db_service.db_connections import MongoDBConnection

from vector_db.db_to_doc import CollectionToDocumentConverter,DynamicDocumentTransformer
from vector_db.streams import fetch_data_stream


def main():
    # ----------------------------
    # DB Connection
    # ----------------------------
    try:
        db_connection = MongoDBConnection()
        db = db_connection.get_database()

        if db is None:
            print("❌ DB connection failed")
            return

        print("✅ Connected to MongoDB")

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return

    # ----------------------------
    # Collections
    # ----------------------------
    try:
        collections = db.list_collection_names()

        if not collections:
            print("⚠️ No collections found")
            return

        print(f"📚 Collections: {collections}")

    except Exception as e:
        print(f"❌ Error fetching collections: {e}")
        return

    # ----------------------------
    # Setup Transformer
    # ----------------------------
    transformer = DynamicDocumentTransformer()
    converter = CollectionToDocumentConverter(transformer)

    # ----------------------------
    # Process Each Collection
    # ----------------------------
    for name in collections:
        print("\n" + "=" * 60)
        print(f"📂 Processing: {name}")

        try:
            collection = db[name]

            stream = fetch_data_stream(collection)

            count = 0

            for doc in converter.convert_stream(stream):
                if count < 2:  # preview only
                    print("\n--- Document ---")
                    print("Content:", doc.page_content[:100])
                    print("Metadata:", doc.metadata)

                count += 1

            print(f"📄 Total documents processed: {count}")

        except Exception as e:
            print(f"❌ Error processing collection {name}: {e}")


if __name__ == "__main__":
    main()