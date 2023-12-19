from unittest.mock import MagicMock
from resources.staffs.staff_models import StaffModel, StaffRspModel
from resources.staffs.staffs_resource import StaffsResource
from resources.staffs.staffs_data_service import StaffDataService

import pytest

@pytest.fixture
def mock_data_service():
    return MagicMock()

@pytest.fixture
def staffs_resource(mock_data_service):
    config = {"data_service": mock_data_service}
    return StaffsResource(config)

def test_get_staffs_no_id(staffs_resource, mock_data_service):
    # Mock the get_staffs return value from data_service
    mock_data_service.get_staffs.return_value = [
        {
            'StaffID': 1,
            'Name': 'John Doe',
            'Position': 'Manager',
            'Email': 'john@example.com',
            'Phone': '1234567890'
        }
    ]
    staffs = staffs_resource.get_staffs()
    assert len(staffs) == 1
    assert isinstance(staffs[0], StaffRspModel)
    mock_data_service.get_staffs.assert_called_once_with(None)

def test_get_staffs_with_id(staffs_resource, mock_data_service):
    StaffID = 1
    mock_data_service.get_staffs.return_value = [
        {
            'StaffID': StaffID,
            'Name': 'John Doe',
            'Position': 'Manager',
            'Email': 'john@example.com',
            'Phone': '1234567890'
        }
    ]
    staffs = staffs_resource.get_staffs(StaffID)
    assert len(staffs) == 1
    assert staffs[0].StaffID == StaffID
    mock_data_service.get_staffs.assert_called_once_with(StaffID)

def test_create_staff(staffs_resource, mock_data_service):
    mock_data_service.create_staff.return_value = 'New Staff Created!'
    result = staffs_resource.create_staff("John Doe", "Manager", "john@example.com", "1234567890")
    assert result == 'New Staff Created!'
    mock_data_service.create_staff.assert_called_once()

