from resources.abstract_base_data_service import BaseDataService
import json
from resources.meetings.meeting_models import MeetingModel, MeetingRspModel
from mysql.connector import Error
import mysql.connector
from datetime import datetime

class MeetingDataService(BaseDataService):

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

    def get_meetings(self, MeetingID: int = None):
        if MeetingID is None:
            select_data_query = """SELECT * FROM Meeting;"""
            rows, json_result = self.execute_read_query(self.db, select_data_query)
        else:
            select_data_query = """SELECT * FROM Meeting WHERE MeetingID=%s;"""
            rows, json_result = self.execute_read_query(self.db, select_data_query, (MeetingID,))
        return json_result

    def create_meeting(self, StaffID: int, ScheduledTime: datetime, Agenda: str):
        meeting_data = dict(StaffID=StaffID, ScheduledTime=ScheduledTime, Agenda=Agenda)
        insert_query = """INSERT INTO Meeting (StaffID, ScheduledTime, Agenda) VALUES (%s, %s, %s);"""
        self.execute_write_query(self.db, insert_query, (meeting_data["StaffID"], meeting_data["ScheduledTime"],
                                                         meeting_data["Agenda"]))

        return "New Meeting Created!"

    def change_agenda(self, MeetingID: int, Agenda: str):
        select_data_query = """SELECT * FROM Meeting WHERE MeetingID=%s;"""
        rows, json_result = self.execute_read_query(self.db, select_data_query, (MeetingID,))
        if json_result == []:
            return "Meeting with MeetingID {} does not exist.".format(MeetingID)

        change_agenda_query = """UPDATE Meeting SET Agenda = %s WHERE MeetingID=%s;"""
        self.execute_write_query(self.db, change_agenda_query, (Agenda, MeetingID))

        return "Meeting {} Agenda Changed!".format(MeetingID)

    def delete_meeting(self, MeetingID: int):
        select_data_query = """SELECT * FROM Meeting WHERE MeetingID=%s;"""
        rows, json_result = self.execute_read_query(self.db, select_data_query, (MeetingID,))
        if json_result == []:
            return "Meeting with MeetingID {} does not exist.".format(MeetingID)

        delete_query = """DELETE FROM Meeting WHERE MeetingID=%s;"""
        self.execute_write_query(self.db, delete_query, (MeetingID,))

        return "Meeting with MeetingID {} is deleted.".format(MeetingID)

