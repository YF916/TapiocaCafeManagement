import pytest
from datetime import datetime
from unittest.mock import MagicMock
from resources.staffs.staffs_data_service import StaffDataService

@pytest.fixture
def mock_db_connection():
    return MagicMock()

@pytest.fixture
def staff_service(mock_db_connection):
    config = {"db_connection": mock_db_connection}
    return StaffDataService(config)

def test_get_staffs_no_id(staff_service, mock_db_connection):
    # Mock the execute_read_query return value
    mock_db_connection.cursor.return_value.fetchall.return_value = []
    staffs = staff_service.get_staffs()
    assert staffs == []
    mock_db_connection.cursor.return_value.execute.assert_called_once()

def test_get_staffs_with_id(staff_service, mock_db_connection):
    StaffID = 1
    mock_db_connection.cursor.return_value.fetchall.return_value = []
    staffs = staff_service.get_staffs(StaffID)
    assert staffs == []
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        """SELECT * FROM Staff WHERE StaffID=%s;""", (StaffID,))

def test_create_staff(staff_service, mock_db_connection):
    result = staff_service.create_staff("John Doe", "Manager", "john@example.com", "1234567890")
    assert result == "New Staff Created!"
    mock_db_connection.cursor.return_value.execute.assert_called_once()

# Add tests for get_staffs_pagination, change_position, and delete_staff methods

