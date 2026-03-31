""""
built this helper to stream data from MongoDB safely, without loading everything into memory at once.

"""
def fetch_data_stream(collection, batch_size=100):
    """
    Stream data from MongoDB safely.
    """
    try:
        cursor = collection.find().batch_size(batch_size)
        for record in cursor:
            yield record
    except Exception as e:
        print(f" Error fetching data: {e}")