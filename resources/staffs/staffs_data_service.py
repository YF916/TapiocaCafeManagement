from resources.abstract_base_data_service import BaseDataService
import json
from resources.staffs.staff_models import StaffModel, StaffRspModel
from mysql.connector import Error
import mysql.connector
from datetime import datetime

class StaffDataService(BaseDataService):

    def __init__(self, config: dict):
        super().__init__()
        self.db = config["db_connection"]

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

    def datetime_converter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

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

            json_result = json.dumps(result, default=self.datetime_converter, indent=4)
            json_dict = json.loads(json_result)

            return rows, json_dict
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_staffs(self, StaffID: int = None):
        if StaffID is None:
            select_data_query = """SELECT * FROM Staff;"""
            rows, json_result = self.execute_read_query(self.db, select_data_query)
        else:
            select_data_query = """SELECT * FROM Staff WHERE StaffID=%s;"""
            rows, json_result = self.execute_read_query(self.db, select_data_query, (StaffID,))
        return json_result

    def get_staffs_pagination(self, StaffID=None, limit: int = 5, offset: int = 0):
        #offset = (page_number - 1) * page_size
        if StaffID is None:
            select_data_query = "SELECT * FROM Staff LIMIT %s OFFSET %s;"
            rows, json_result = self.execute_read_query(self.db, select_data_query, (limit, offset))
        else:
            select_data_query = "SELECT * FROM Staff WHERE StaffID = %s LIMIT %s OFFSET %s;"
            rows, json_result = self.execute_read_query(self.db, select_data_query, (StaffID, limit, offset))

        return json_result

    def create_staff(self, Name: str, Position: str , Email: str, Phone: str):
        staff_data = dict(Name=Name, Position=Position, Email=Email, Phone=Phone)
        insert_query = """INSERT INTO Staff (Name, Position, Email, Phone) VALUES (%s, %s, %s, %s);"""
        self.execute_write_query(self.db, insert_query, (staff_data["Name"], staff_data["Position"],
                                                         staff_data["Email"], staff_data["Phone"]))

        return "New Staff Created!"

    def change_position(self, StaffID: int, Position: str):
        select_data_query = """SELECT * FROM Staff WHERE StaffID=%s;"""
        rows, json_result = self.execute_read_query(self.db, select_data_query, (StaffID,))
        if json_result == []:
            return "Staff with StaffID {} does not exist.".format(StaffID)

        change_agenda_query = """UPDATE Staff SET Position = %s WHERE StaffID=%s;"""
        self.execute_write_query(self.db, change_agenda_query, (Position, StaffID))

        return "Staff {} Position Changed!".format(StaffID)

    def delete_staff(self, StaffID: int):
        select_data_query = """SELECT * FROM Staff WHERE StaffID=%s;"""
        rows, json_result = self.execute_read_query(self.db, select_data_query, (StaffID,))
        if json_result == []:
            return "Staff with StaffID {} does not exist.".format(StaffID)

        delete_query = """DELETE FROM Staff WHERE StaffID=%s;"""
        self.execute_write_query(self.db, delete_query, (StaffID,))

        return "Staff with StaffID {} is deleted.".format(StaffID)

