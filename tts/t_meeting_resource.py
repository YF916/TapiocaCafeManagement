import pytest
from unittest.mock import MagicMock
from datetime import datetime
from resources.meetings.meeting_models import MeetingRspModel, MeetingModel
from resources.meetings.meetings_resource import MeetingsResource

@pytest.fixture
def mock_data_service():
    return MagicMock()

@pytest.fixture
def meetings_resource(mock_data_service):
    config = {"data_service": mock_data_service}
    return MeetingsResource(config)

def test_get_meetings_no_id(meetings_resource, mock_data_service):
    mock_data_service.get_meetings.return_value = [{"MeetingID": 1, "StaffID": 2, "ScheduledTime": datetime.now(), "Agenda": "Test Agenda"}]
    meetings = meetings_resource.get_meetigs()
    assert len(meetings) == 1
    assert isinstance(meetings[0], MeetingRspModel)
    mock_data_service.get_meetings.assert_called_once_with(None)

def test_get_meetings_with_id(meetings_resource, mock_data_service):
    MeetingID = 1
    mock_data_service.get_meetings.return_value = [{"MeetingID": MeetingID, "StaffID": 2, "ScheduledTime": datetime.now(), "Agenda": "Test Agenda"}]
    meetings = meetings_resource.get_meetigs(MeetingID)
    assert len(meetings) == 1
    assert meetings[0].MeetingID == MeetingID
    mock_data_service.get_meetings.assert_called_once_with(MeetingID)


# Add tests for change_agenda and delete_meeting methods

