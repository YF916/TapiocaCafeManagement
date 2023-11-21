from __future__ import annotations
from pydantic import BaseModel
from typing import List
from resources.rest_models import Link
from datetime import datetime

class StaffModel(BaseModel):
    StaffID: int
    Name: str
    Position: str # Manager, Front Desk, Chef
    Email: str
    Phone: str

model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "StaffID": 1,
                    "Name": "Amy",
                    "Position": "Manager",
                    "Email": "123@example.com",
                    "Phone": "9999999999"
                }
            ]
        }
    }


class StaffRspModel(StaffModel):
    links: List[Link] = None



