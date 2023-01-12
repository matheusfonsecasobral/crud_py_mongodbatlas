import pymongo as pymongo


class DbConnection:
    client = pymongo.MongoClient(
        "mongodb+srv://root:root@cluster0.hibkye9.mongodb.net/?retryWrites=true&w=majority")
    products = client['StockSystemDB']['products']
