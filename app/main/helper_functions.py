from .. import master_flash_db_client

def is_document_present(collection, query):
    clients = master_flash_db_client[collection]
    results = clients.find_one(query)
    print("Results of query :: ", results)
    return results is not None

