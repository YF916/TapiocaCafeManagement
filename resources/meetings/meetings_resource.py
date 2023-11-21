from resources.abstract_base_resource import BaseResource
from resources.meetings.meeting_models import MeetingModel, MeetingRspModel
from resources.rest_models import Link
from typing import List
from datetime import datetime

class MeetingsResource(BaseResource):
    def __init__(self, config):
        super().__init__()

        self.data_service = config["data_service"]

    @staticmethod
    def _generate_links(s: dict) -> MeetingRspModel:
        self_link = Link(**{
            "rel": "self",
            "href": "/meetings/" + str(s['MeetingID'])
        })

        links = [
            self_link,
        ]
        rsp = MeetingRspModel(**s, links=links)
        return rsp

    def get_meetigs(self, MeetingID: int = None) -> List[MeetingRspModel]:

        result = self.data_service.get_meetings(MeetingID)
        final_result = []

        for s in result:
            m = self._generate_links(s)
            final_result.append(m)

        return final_result

    def create_meeting(self, StaffID: int, ScheduledTime: datetime, Agenda: str):
        result = self.data_service.create_meeting(StaffID=StaffID, ScheduledTime=ScheduledTime, Agenda=Agenda)
        return result

    def change_agenda(self, MeetingID: int, Agenda: str):
        result = self.data_service.change_agenda(MeetingID=MeetingID, Agenda=Agenda)
        return result

    def delete_meeting(self, MeetingID: int):
        result = self.data_service.delete_meeting(MeetingID=MeetingID)
        return result
