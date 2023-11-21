from resources.abstract_base_data_service import BaseDataService
import json
from resources.products.product_models import ProductModel, ProductRspModel
from mysql.connector import Error
import mysql.connector
from decimal import Decimal

class ProductDataService(BaseDataService):

    def __init__(self, config: dict):
        """

        :param config: A dictionary of configuration parameters.
        """
        super().__init__()

        # self.data_dir = config['data_directory']
        # self.data_file = config["data_file"]

        self.db = config["db_connection"]
        #self.products = []

        #self._load()

    # def _get_data_file_name(self):
    #     # DFF TODO Using os.path is better than string concat
    #     # result = self.data_dir + "/" + self.data_file
    #     result = self.db
    #
    #     return result

    # def _load(self):
    #
    #     fn = self._get_data_file_name()
    #     with open(fn, "r") as in_file:
    #         self.products = json.load(in_file)
    #
    # def _save(self):
    #     fn = self._get_data_file_name()
    #     with open(fn, "w") as out_file:
    #         json.dump(self.products, out_file, indent=2)
    def execute_write_query(self, connection, query, params=None):
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)  # or use str(obj) if you want to preserve exactness
            return json.JSONEncoder.default(self, obj)

    def execute_read_query(self, connection, query, params=None):
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]

            json_result = json.dumps(result, cls=self.DecimalEncoder, indent=4)
            json_dict = json.loads(json_result)

            return rows, json_dict
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_products(self,  ProductID: int = None):
        # result = []
        #
        # for s in self.products:
        #     if (ProductID is None or (s.get("ProductID", None) == ProductID)):
        #         result.append(s)
        # return result
        if ProductID is None:
            select_data_query = """SELECT * FROM Product;"""
            rows, json_result = self.execute_read_query(self.db, select_data_query)
        else:
            select_data_query = """SELECT * FROM Product WHERE ProductID=%s;"""
            rows, json_result = self.execute_read_query(self.db, select_data_query, (ProductID,))
        return json_result

    def create_product(self, Name: str, Category: str, Price: float, Threshold: int, Quantity: int):

        # existing_product = next((p for p in self.products if p['ProductID'] == ProductID), None)
        # if existing_product is not None:
        #     return "Product with ProductID {} already exists.".format(ProductID)
        #
        # product_data = dict(ProductID=ProductID, Name=Name, Category=Category, Price=Price, Threshold=Threshold,
        #                     Quantity=Quantity)
        # self.products.append(product_data)
        # self._save()
        product_data = dict(Name=Name, Category=Category, Price=Price, Threshold=Threshold,
                            Quantity=Quantity)

        insert_query = """INSERT INTO Product (Name, Category, Price, Threshold, Quantity) VALUES (%s, %s, %s, %s, %s);"""

        self.execute_write_query(self.db, insert_query, (product_data["Name"], product_data["Category"],
                                                         product_data["Price"], product_data["Threshold"], product_data["Quantity"]))

        return "New Product Created!"


    def change_quantity(self, ProductID: int, num: int):
        # existing_product = next((p for p in self.products if p['ProductID'] == ProductID), None)
        # if existing_product is None:
        #     return "Product with ProductID {} does not exist.".format(ProductID)
        #
        # result = None
        # for i, product in enumerate(self.products):
        #     if product["ProductID"] == ProductID:
        #         product["Quantity"]  += num
        #         result = product
        #         self.products[i].update(product)
        #         self._save()

        select_data_query = """SELECT * FROM Product WHERE ProductID=%s;"""
        rows, json_result = self.execute_read_query(self.db, select_data_query, (ProductID,))
        if json_result == []:
            return "Product with ProductID {} does not exist.".format(ProductID)

        change_quantity_query = """UPDATE Product SET Quantity = Quantity + %s WHERE ProductID=%s;"""
        self.execute_write_query(self.db, change_quantity_query, (num, ProductID))

        return "Product {} Quantity Changed!".format(ProductID)

    def change_price(self, ProductID: int, new_price: float):
        # existing_product = next((p for p in self.products if p['ProductID'] == ProductID), None)
        # if existing_product is None:
        #     return "Product with ProductID {} does not exist.".format(ProductID)
        #
        # result = None
        # for i, product in enumerate(self.products):
        #     if product["ProductID"] == ProductID:
        #         product["Price"]  = new_price
        #         result = product
        #         self.products[i].update(product)
        #         self._save()
        #
        # return result
        select_data_query = """SELECT * FROM Product WHERE ProductID=%s;"""
        rows, json_result = self.execute_read_query(self.db, select_data_query, (ProductID,))
        if json_result == []:
            return "Product with ProductID {} does not exist.".format(ProductID)

        change_price_query = """UPDATE Product SET Price = %s WHERE ProductID=%s;"""
        self.execute_write_query(self.db, change_price_query, (new_price, ProductID))

        return "Product {} Price Changed!".format(ProductID)

    def delete_product(self, ProductID: int):
        # existing_product = next((p for p in self.products if p['ProductID'] == ProductID), None)
        # if existing_product is None:
        #     return "Product with ProductID {} does not exist.".format(ProductID)
        #
        # for i, product in enumerate(self.products):
        #     if product["ProductID"] == ProductID:
        #         del self.products[i]
        #         self._save()
        #         return "Product with ProductID {} is deleted.".format(ProductID)
        # return "Failed to delete Product with ProductID {}.".format(ProductID)

        select_data_query = """SELECT * FROM Product WHERE ProductID=%s;"""
        rows, json_result = self.execute_read_query(self.db, select_data_query, (ProductID,))
        if json_result == []:
            return "Product with ProductID {} does not exist.".format(ProductID)

        delete_query = """DELETE FROM Product WHERE ProductID=%s;"""
        self.execute_write_query(self.db, delete_query, (ProductID,))

        return "Product with ProductID {} is deleted.".format(ProductID)





