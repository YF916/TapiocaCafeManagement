#
# FastAPI is a framework and library for implementing REST web services in Python.
# https://fastapi.tiangolo.com/
#
import json
from datetime import datetime

from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from typing import List, Union
from resources.rest_models import Link

# I like to launch directly and not use the standard FastAPI startup process.
# So, I include uvicorn
import uvicorn


from resources.products.product_models import ProductModel, ProductRspModel
from resources.products.products_resource import ProductsResource
from resources.products.products_data_service import ProductDataService

from resources.meetings.meeting_models import MeetingRspModel, MeetingModel
from resources.meetings.meetings_resource import MeetingsResource
from resources.meetings.meetings_data_service import MeetingDataService

from resources.staffs.staff_models import StaffModel, StaffRspModel
from resources.staffs.staffs_resource import StaffsResource
from resources.staffs.staffs_data_service import StaffDataService

import os
from mysql.connector import Error
import mysql.connector

def create_database(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_database_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_write_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()
def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        column_names = [column[0] for column in cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]

        json_result = json.dumps(result, default=datetime_converter, indent=4)

        return rows, json_result
    except Error as e:
        print(f"The error '{e}' occurred")

class ProductRspModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ProductRspModel):
            # Convert ProductRspModel to a serializable format
            return obj.__dict__  # or a custom representation
        elif isinstance(obj, Link):
            # Convert Link to a serializable format
            return obj.__dict__  # assuming Link has attributes to serialize
        return json.JSONEncoder.default(self, obj)

class MeetingRspModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MeetingRspModel):
            # Convert ProductRspModel to a serializable format
            return obj.__dict__  # or a custom representation
        elif isinstance(obj, Link):
            # Convert Link to a serializable format
            return obj.__dict__  # assuming Link has attributes to serialize
        return json.JSONEncoder.default(self, obj)

class StaffRspModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StaffRspModel):
            # Convert ProductRspModel to a serializable format
            return obj.__dict__  # or a custom representation
        elif isinstance(obj, Link):
            # Convert Link to a serializable format
            return obj.__dict__  # assuming Link has attributes to serialize
        return json.JSONEncoder.default(self, obj)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def hello_world():
    return 'Hello, from Docker! I am Tapioca Cafe Management Service.'

def get_data_service():
    # db_connection = create_database_connection(
    #     host_name="database-demo-1.cuaeupdge24w.us-east-2.rds.amazonaws.com",
    #     user_name = "admin",
    #     user_password = "sfIM25PoEzLDlPriyzNw",
    #     db_name = "my_database"
    # )

    db_connection = create_database_connection(
        host_name="database-1.caogqwqgw2no.us-east-1.rds.amazonaws.com",
        user_name="admin",
        user_password="Stargod08122",
        db_name="Tapioca"
    )

    if db_connection is None:
        raise Exception("Failed to connect to the database")

    config = {
        # "data_directory": os.getcwd() + "/data/",
        # "data_file": "products.json"

        "db_connection": db_connection
    }

    ds_prod = ProductDataService(config)
    ds_mt = MeetingDataService(config)
    ds_sf = StaffDataService(config)
    return ds_prod, ds_mt, ds_sf


def get_resource():
    ds_prod, ds_mt, ds_sf = get_data_service()
    config_prod = {
        "data_service": ds_prod
    }
    res_prod = ProductsResource(config_prod)

    config_mt = {
        "data_service": ds_mt
    }
    res_mt = MeetingsResource(config_mt)

    config_sf = {
        "data_service": ds_sf
    }
    res_sf = StaffsResource(config_sf)

    return res_prod, res_mt, res_sf


products_resource, meetings_resource, staffs_resource = get_resource()



@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")

@app.get("/cafe/products", response_model=Union[ProductRspModel, None, List[ProductRspModel], str])
async def get_products(ProductID: int = None):
    result = products_resource.get_products(ProductID)
    if len(result) == 1:
        result = result[0]
    return result

@app.get("/cafe/products/{ProductID}", response_model=Union[ProductRspModel, None])
async def get_product(ProductID: int):

    result = None
    result = products_resource.get_products(ProductID)
    if len(result) == 1:
        result = result[0]
    else:
        raise HTTPException(status_code=404, detail="Not found")

    return result

@app.post("/cafe/products/create", response_model=Union[ProductRspModel, str])
async def create_product(Name: str, Category: str, Price: float, Threshold: int, Quantity: int):
    result = None
    result = products_resource.create_product(Name=Name, Category=Category, Price=Price, Threshold=Threshold,
                                   Quantity=Quantity)
    return result
#
@app.put("/cafe/products/change_quantity", response_model=Union[ProductRspModel, str])
async def change_quantity(ProductID: int, num: int):
    result = None
    result = products_resource.change_quantity(ProductID=ProductID, num=num)
    return result
#
@app.put("/cafe/products/change_price", response_model=Union[ProductRspModel, str])
async def change_price(ProductID: int, new_price: float):
    result = None
    result = products_resource.change_price(ProductID=ProductID, new_price=new_price)
    return result
#
@app.delete("/cafe/products/delete/", response_model=Union[str])
async def delete_product(ProductID: int):
    result = products_resource.delete_product(ProductID=ProductID)
    return result


@app.get("/cafe/meetings", response_model=List[MeetingRspModel])
async def get_meetings(MeetingID: int = None):
    result = meetings_resource.get_meetigs(MeetingID)
    return result

@app.post("/cafe/meetings/create", response_model=Union[MeetingRspModel, str])
async def create_product(StaffID: int, ScheduledTime: datetime, Agenda: str):
    result = meetings_resource.create_meeting(StaffID=StaffID, ScheduledTime=ScheduledTime, Agenda=Agenda)
    return result

@app.put("/cafe/meetings/change_agenda", response_model=Union[MeetingRspModel, str])
async def change_agenda(MeetingID: int, Agenda: str):
    result = meetings_resource.change_agenda(MeetingID=MeetingID, Agenda=Agenda)
    return result
#
@app.delete("/cafe/meetings/delete/", response_model=Union[str])
async def delete_meeting(MeetingID: int):
    result = meetings_resource.delete_meeting(MeetingID=MeetingID)
    return result


@app.get("/cafe/staffs", response_model=List[StaffRspModel])
async def get_staffs(StaffID: int = None):
    result = staffs_resource.get_staffs(StaffID)
    return result


@app.get("/cafe/staffs_pagination", response_model=List[StaffRspModel])
async def get_staffs_pagination(StaffID: int =None, limit: int = 5, offset: int = 0):
    result = staffs_resource.get_staffs_pagination(StaffID, limit, offset)
    return result

@app.post("/cafe/staffs/create", response_model=Union[StaffRspModel, str])
async def create_staff(Name: str, Position: str , Email: str, Phone: str):
    result = staffs_resource.create_staff(Name=Name, Position=Position, Email=Email, Phone=Phone)
    return result

@app.put("/cafe/staffs/change_position", response_model=Union[StaffRspModel, str])
async def change_position(StaffID: int, Position: str):
    result = staffs_resource.change_position(StaffID=StaffID, Position=Position)
    return result
#
@app.delete("/cafe/staffs/delete/", response_model=Union[str])
async def delete_staff(StaffID: int):
    result = staffs_resource.delete_staff(StaffID=StaffID)
    return result

# @app.get("/schools", response_model=List[SchoolRspModel])
# async def get_schools():
#     """
#     Return a list of schools.
#     """
#     result = schools_resource.get_schools()
#     return result
#
#
# @app.get("/schools/{school_code}/students", response_model=List[StudentRspModel])
# async def get_schools_students(school_code, uni=None, last_name=None):
#     """
#     Return a list of schools.
#     """
#     result = schools_resource.get_schools_students(school_code, uni, last_name)
#     return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
    #
    #
    #
    #
    # host = "database-demo-1.cuaeupdge24w.us-east-2.rds.amazonaws.com"
    # user = "admin"
    # password = "sfIM25PoEzLDlPriyzNw"
    #
    # #connection = create_database(host_name=host, user_name=user, user_password=password)
    #
    # create_database_query = """
    #       CREATE DATABASE my_database;
    #       """
    # #execute_write_query(connection, create_database_query)
    #
    # show_database_query = """ SHOW DATABASES; """
    # #execute_read_query(connection, show_database_query)
    #

    # database = "my_database"
    # connection = create_database_connection(host_name=host, user_name=user, user_password=password, db_name=database)
    # create_table_query = """
    # CREATE TABLE IF NOT EXISTS meetings (
    #     MeetingID INT AUTO_INCREMENT,
    #     StaffID INT,
    #     ScheduledTime DATETIME,
    #     Agenda TEXT,
    #     PRIMARY KEY (MeetingID),
    #     FOREIGN KEY (StaffID) REFERENCES staffs(StaffID)
    # );
    # """
    # execute_write_query(connection, create_table_query)
    #
    # insert_data_query = """
    # INSERT INTO meetings (StaffID, ScheduledTime, Agenda)
    # VALUES (1, '2023-03-15 10:00:00', 'Discuss project timeline'),
    #        (2, '2023-03-16 14:00:00', 'Budget review meeting');
    # """
    # execute_write_query(connection, insert_data_query)

    # select_data_query = """
    #    SELECT * FROM meetings;
    #    """
    # rows, json_result = execute_read_query(connection, select_data_query)
    # print(rows)
    # print(json_result)

