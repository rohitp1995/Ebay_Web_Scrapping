import pymongo
import pandas as pd
import json
import ssl


class MongodbOperations:
    def __init__(self, Username, Password):
        """
        This function sets the Url for Mongo db cloud Connection
        :param Username:
        :param Password:
        """
        try:
            self.Username = Username
            self.Password = Password
            self.url = f"mongodb://{self.Username}:{self.Password}@cluster0-shard-00-00.hmgxe.mongodb.net:27017,cluster0-shard-00-01.hmgxe.mongodb.net:27017,cluster0-shard-00-02.hmgxe.mongodb.net:27017/test?replicaSet=atlas-d5lub3-shard-0&ssl=true&authSource=admin"
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initiation process\n" + str(e))

    def MongoClientConnection(self):
        """
        This establish a connection with cloud database for Mongodb
        """
        try:
            cloud_client = pymongo.MongoClient(self.url, ssl_cert_reqs=ssl.CERT_NONE)
            return cloud_client
        except Exception as e:
            rasie
            Exception("(MongoClientConnection): Something went wrong with client connection with cloud\n" + str(e))

    def IsdatabasePresent(self, database_name):
        """
        This function will tell if the database is currently present or not in our cluster
        """

        try:
            client = self.MongoClientConnection()
            if database_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise Exception("(IsdatabasePresent): Something went wrong when searching for database name\n" + str(e))

    def getDatabase(self, db_name):
        """
        This returns databases.
        """
        try:
            database_check = self.IsdatabasePresent(database_name=db_name)
            if database_check:
                mongo_client = self.MongoClientConnection()
                return mongo_client[db_name]
            else:
                return "no such database present"
        except Exception as e:
            raise Exception(f"(getDatabase): Failed to get the database list")

    def CreateDatabase(self, db_name):
        """
        This function checks and create database if it is not available
        """
        try:
            database_check = self.IsdatabasePresent(database_name=db_name)
            if not database_check:
                mongo_client = self.MongoClientConnection()
                database = mongo_client[db_name]
                collection = database['temp_table']
                record = {'a': 1}
                collection.insert_one(record)
                return database
            else:
                mongo_client = self.MongoClientConnection()
                database = mongo_client[db_name]

                return database
        except Exception as e:
            raise Exception('(CreateDatabase): Something went wrong while creating the database\n' + str(e))


    def DropDatabase(self, db_name):
        """
        This function drops the database
        """
        try:
            database_check = self.IsdatabasePresent(database_name=db_name)
            if database_check:
                mongo_client = self.MongoClientConnection()
                mongo_client.dropDatabase(db_name)
                return f"{db_name} Dropped from cloud server"
            else:
                return f"{db_name} does not exist in the cloud server"

        except Exception as e:
            raise Exception('(DropDatabase): Something went wrong while dropping database\n' + str(e))


    def CheckCollectionExistence(self, db_name, collection_name):
        """
        This function will check if the collection exists or not
        """

        try:
            mongo_client = self.MongoClientConnection()
            database_check = self.IsdatabasePresent(database_name=db_name)
            if database_check:
                database = self.getDatabase(db_name=db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception("(CheckCollectionExistence): Something went wrong while searching for collection",
                            + str(e))


    def CreateCollection(self, db_name, name_of_collection):
        """
        This function will create the collection if it exists in the database
        """
        try:
            check_database = self.IsdatabasePresent(database_name=db_name)
            if check_database:
                collection_check = self.CheckCollectionExistence(db_name, name_of_collection)
                if not collection_check:
                    database = self.getDatabase(db_name)
                    name_of_collection = database.create_collection(name_of_collection)
                    return name_of_collection
                else:
                    return f"Collection {name_of_collection}  Already Exists"
            else:
                return "Couldn't find the database"
        except Exception as e:
            raise Exception("(CreateCollection): Something went wrong with creation of Collection" + str(e))


    def DropCollectionIfExist(self, db_name, collection_name):
        """
        This function will drop the collection if it exists in the database
            """
        try:
            check_database = self.IsdatabasePresent(database_name=db_name)
            if check_database:
                database = self.getDatabase(db_name)
                if collection_name in database.list_collection_names():
                    collection = database[collection_name]
                    collection.drop()
                    return "Collection Dropped"
                else:
                    return " no such collection exists"
            else:
                return "Couldn't find the db"
        except Exception as e:
            raise Exception("(DropCollectionIfExist): Something went wrong with dropping of a collection" + str(e))



    def InsertOneRecord(self, db_name, record, collection_name):
        """
        This function will insert a single record
        """
        try:
            check_database = self.IsdatabasePresent(database_name=db_name)
            if check_database:
                database = self.getDatabase(db_name)
                collection_check = self.CheckCollectionExistence(db_name=db_name, collection_name=collection_name)
                if collection_check:
                    collection = database[collection_name]
                    collection.insert_one(record)
                    return "Inserted A record"
                else:
                    return " no such collection exists"
            else:
                return "Couldn't find the database"
        except Exception as e:
            raise Exception(
                "(InsertOneRecord): Something went wrong with Inserting a data into the collection" + str(e))



    def InsertManyRecord(self, db_name, records, collection):
        """
        This function will insert many records at once in the database
        """
        try:
            check_database = self.IsdatabasePresent(db_name=db_name)
            if check_database:
                collection_check = self.CheckCollectionExistence(db_name=db_name, collection_name=collection)
                if collection_check:
                    collection.insert_many(record)
                    return "Inserted records"
                else:
                    return " no such collection exists"
            else:
                return "Couldn't find the database"
        except Exception as e:
            raise Exception(
                "(InsertManyRecord): Something went wrong with Inserting many data into the collection" + str(e))



    def FindOneRecord(self, db_name, collection, query=None):
        """
        This function will find one record from the collection
        """
        try:
            collection_check = self.CheckCollectionExistence(db_name=db_name, collection_name=collection)
            database = database = self.getDatabase(db_name)
            if collection_check:
                collection = database[collection]
                record = collection.find_one(query)
                return record
            else:
                return " no such collection exists"
        except Exception as e:
            raise Exception(
                "(findonerecord): Something went wrong with finding record" + str(
                    e))



    def FindAllRecords(self, db_name, collection):
        """
        This function will find one record from the collection
        """
        try:
            collection_check = self.CheckCollectionExistence(db_name=db_name, collection_name=collection)
            database = database = self.getDatabase(db_name)
            if collection_check:
                collection = database[collection]
                record = list(collection.find())
                return record
            else:
                return " no such collection exists"
        except Exception as e:
            raise Exception("(FindAllRecords): Something went wrong with finding record" + str(e))



    def FindRecordsonQuery(self, db_name, collection, query):
        """
        This function will find record Based on certain Query
        """
        try:
            collection_check = self.CheckCollectionExistence(db_name=db_name, collection_name=collection)
            database = database = self.getDatabase(db_name)
            if collection_check:
                collection = database[collection]
                record = list(collection.find(query))
                return record
            else:
                return " no such collection exists"
        except Exception as e:
            raise Exception("(FindRecordsonQuery): Something went wrong with finding record" + str(e))



    def UpdateOneRecord(self, db_name, collection, present_data, new_data):
        """
        This function will update record Based on new data provided with present data
        """
        try:
            collection_check = self.CheckCollectionExistence(db_name=db_name, collection_name=collection)
            database = database = self.getDatabase(db_name)
            if collection_check:
                collection = database[collection]
                collection.update_one(present_data, new_data)
                logging.info('Collection_updated')
            else:
                return " no such collection exists"
        except Exception as e:
            raise Exception("(UpdateOneRecord): Something went wrong while updating the record" + str(e))



    def UpdateManyRecord(self, db_name, collection, present_data, new_data):
        """
        This function will update record Based on new data provided with present data
        """
        try:
            collection_check = self.CheckCollectionExistence(db_name=db_name, collection_name=collection)
            database = database = self.getDatabase(db_name)
            if collection_check:
                collection = database[collection]
                collection.update_many(present_data, new_data)
                logging.info('Collection_updated')
            else:
                return " no such collection exists"
        except Exception as e:
            raise Exception("(UpdateOneRecord): Something went wrong while updating the records" + str(e))
