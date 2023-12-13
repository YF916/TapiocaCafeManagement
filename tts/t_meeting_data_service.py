# tests/test_meeting_data_service.py
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from resources.meetings.meetings_data_service import MeetingDataService


@pytest.fixture
def mock_db_connection():
    return MagicMock()

@pytest.fixture
def meeting_service(mock_db_connection):
    config = {"db_connection": mock_db_connection}
    return MeetingDataService(config)

def test_get_meetings_no_id(meeting_service, mock_db_connection):
    mock_db_connection.cursor().fetchall.return_value = []
    assert meeting_service.get_meetings() == []
    mock_db_connection.cursor().execute.assert_called_once()

def test_get_meetings_with_id(meeting_service, mock_db_connection):
    MeetingID = 1
    mock_db_connection.cursor().fetchall.return_value = []
    assert meeting_service.get_meetings(MeetingID) == []
    mock_db_connection.cursor().execute.assert_called_once_with(
        """SELECT * FROM Meeting WHERE MeetingID=%s;""", (MeetingID,))

def test_create_meeting(meeting_service, mock_db_connection):
    StaffID = 1
    ScheduledTime = datetime.now()
    Agenda = "Test Agenda"
    response = meeting_service.create_meeting(StaffID, ScheduledTime, Agenda)
    assert response == "New Meeting Created!"
    mock_db_connection.cursor().execute.assert_called_once()

# Additional tests for change_agenda and delete_meeting would follow a similar pattern

