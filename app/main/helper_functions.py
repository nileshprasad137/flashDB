from .. import mongo_client

def is_document_present(collection, query, database="flashdb"):
    collection_connection = mongo_client[database][collection]
    results = collection_connection.find_one(query)
    print("Results of query :: ", results)
    return results is not None

