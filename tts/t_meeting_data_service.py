import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from resources.meetings.meeting_models import MeetingModel, MeetingRspModel
from resources.meetings.meetings_data_service import MeetingDataService

class TestMeetingDataService(unittest.TestCase):

    def setUp(self):
        self.mock_db_connection = MagicMock()
        self.config = {"db_connection": self.mock_db_connection}
        self.meeting_service = MeetingDataService(self.config)

    @patch('resources.meetings.meetings_data_service.MeetingDataService.execute_read_query')
    def test_get_meetings_no_id(self, mock_execute_read_query):
        mock_execute_read_query.return_value = ([], [])
        meetings = self.meeting_service.get_meetings()
        self.assertEqual(meetings, [])
        mock_execute_read_query.assert_called_once()

    @patch('resources.meetings.meetings_data_service.MeetingDataService.execute_read_query')
    def test_get_meetings_with_id(self, mock_execute_read_query):
        mock_execute_read_query.return_value = ([], [])
        MeetingID = 1
        meetings = self.meeting_service.get_meetings(MeetingID)
        self.assertEqual(meetings, [])
        mock_execute_read_query.assert_called_once_with(self.mock_db_connection,
                                                        """SELECT * FROM Meeting WHERE MeetingID=%s;""",
                                                        (MeetingID,))

    @patch('resources.meetings.meetings_data_service.MeetingDataService.execute_write_query')
    def test_create_meeting(self, mock_execute_write_query):
        StaffID = 1
        ScheduledTime = datetime.now()
        Agenda = "Test Agenda"
        response = self.meeting_service.create_meeting(StaffID, ScheduledTime, Agenda)
        self.assertEqual(response, "New Meeting Created!")
        mock_execute_write_query.assert_called_once()

    # Add more tests for change_agenda and delete_meeting methods

if __name__ == '__main__':
    unittest.main()
