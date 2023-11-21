from __future__ import annotations
from pydantic import BaseModel
from typing import List
from resources.rest_models import Link
from datetime import datetime

class MeetingModel(BaseModel):
    MeetingID: int
    StaffID: int
    ScheduledTime: datetime
    Agenda: str


model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "MeetingID": 1,
                    "StaffID": 1,
                    "ScheduledTime": "2023-03-15 10:00:00",
                    "Agenda": "Discuss project timeline"
                }
            ]
        }
    }


class MeetingRspModel(MeetingModel):
    links: List[Link] = None



