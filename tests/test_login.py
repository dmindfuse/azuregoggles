import pytest
from unittest.mock import patch, MagicMock
from my_app.controllers.login import LoginController

@patch('subprocess.run')
def test_login(mock_subprocess):
    mock_subprocess.return_value = MagicMock(stdout='https://microsoft.com/devicelogin and enter the code ABC123DEF')
    
    login_controller = LoginController()
    login_controller.login()
    
    mock_subprocess.assert_called_with(['az', 'login', '--use-device-code'], capture_output=True, text=True)

