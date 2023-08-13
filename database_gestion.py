from pymongo import MongoClient

def get_best_documents(selected_class, selected_main_spe):
    # Connect to your MongoDB database
    db, client = get_database()
    collection = db['Players']

    # Search for the 20 best documents that match the selected class and main_spe,
    # sorted by 'lvl_spe' in descending order
    pipeline = [
        {'$match': {'Classe': selected_class, 'Main_spe': selected_main_spe, 'Guilde': ''}},
        {'$sort': {'lvl_spe': -1}},
        {'$limit': 20}
    ]
    cursor = collection.aggregate(pipeline)
    print(cursor)

    return list(cursor)

def get_all_classes():
    # Connect to your MongoDB database
    db, client = get_database()
    collection = db['Players']

    # Get all unique values of 'Classe' from the collection
    classes = sorted(collection.distinct('Classe'))

    return classes

def get_main_spe_by_class(selected_class):
    # Connect to your MongoDB database
    db, client = get_database()
    collection = db['Players']

    # Search for all possible 'Main_spe' values that contain the selected class and are not empty or None
    pipeline = [
        {'$match': {'Classe': selected_class, 'Main_spe': {'$ne': None, '$ne': ''}}}
    ]
    cursor = collection.aggregate(pipeline)

    main_spe_values = sorted(list({doc['Main_spe'] for doc in cursor}))

    return main_spe_values

def update_documents_in_db(dict_arr):
    db, client = get_database()
    collection = db['Players']

    for doc in dict_arr:
        existing_doc = collection.find_one({'Serveur': doc['Serveur'], 'Nom du joueur': doc['Nom du joueur']})

        if existing_doc is None:
            # If no document with the same 'Serveur' and 'Nom du joueur' exists, insert the new document
            collection.insert_one(doc)
        else:
            # If a document with the same 'Serveur' and 'Nom du joueur' exists, compare and update values
            if doc['Main_spe'] != existing_doc['Main_spe'] and doc['Main_spe'] != "":
                collection.update_one(
                    {'_id': existing_doc['_id']},
                    {'$set': {'Main_spe': doc['Main_spe']}}
                )

            if doc['lvl_spe'] != existing_doc['lvl_spe'] and doc['lvl_spe'] > 0:
                collection.update_one(
                    {'_id': existing_doc['_id']},
                    {'$set': {'lvl_spe': doc['lvl_spe']}}
                )

    client.close()

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://CanardWc:Tentionarve47@censusplusdata.aizzrg4.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
  
   try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
   except Exception as e:
    print(e)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['censusplusdata'], client