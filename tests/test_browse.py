import pytest
from unittest.mock import patch, MagicMock
from my_app.controllers.browse import BrowseController

@patch('subprocess.run')
@patch('builtins.input', side_effect=['q'])
def test_browse(mock_input, mock_subprocess):
    mock_subprocess.return_value = MagicMock(stdout='[{"name": "file1.txt", "properties": {"lastModified": "2025-01-01T00:00:00Z", "contentLength": 123}}]')
    
    browse_controller = BrowseController()
    browse_controller.browse()
    
    mock_subprocess.assert_called_with(
        ['az', 'storage', 'blob', 'list', 
        '--account-name', 'mystorageaccount', 
        '--container-name', 'mycontainer', 
        '--prefix', '/',
        '--output', 'json'], 
        capture_output=True, text=True
    )
    mock_input.assert_called()
