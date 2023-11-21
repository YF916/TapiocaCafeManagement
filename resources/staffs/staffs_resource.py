from resources.abstract_base_resource import BaseResource
from resources.staffs.staff_models import StaffModel, StaffRspModel
from resources.rest_models import Link
from typing import List
from datetime import datetime

class StaffsResource(BaseResource):
    def __init__(self, config):
        super().__init__()

        self.data_service = config["data_service"]

    @staticmethod
    def _generate_links(s: dict) -> StaffRspModel:
        self_link = Link(**{
            "rel": "self",
            "href": "/staffs/" + str(s['StaffID'])
        })

        links = [
            self_link,
        ]
        rsp = StaffRspModel(**s, links=links)
        return rsp

    def get_staffs(self, StaffID: int = None) -> List[StaffRspModel]:

        result = self.data_service.get_staffs(StaffID)
        final_result = []

        for s in result:
            m = self._generate_links(s)
            final_result.append(m)

        return final_result

    def get_staffs_pagination(self, StaffID=None, limit: int = 5, offset: int = 0) -> List[StaffRspModel]:

        result = self.data_service.get_staffs_pagination(StaffID, limit, offset)
        final_result = []

        for s in result:
            m = self._generate_links(s)
            final_result.append(m)

        return final_result

    def create_staff(self, Name: str, Position: str , Email: str, Phone: str):
        result = self.data_service.create_staff(Name=Name, Position=Position, Email=Email, Phone=Phone)
        return result

    def change_position(self, StaffID: int, Position: str):
        result = self.data_service.change_position(StaffID=StaffID, Position=Position)
        return result

    def delete_staff(self, StaffID: int):
        result = self.data_service.delete_staff(StaffID=StaffID)
        return result
