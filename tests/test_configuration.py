import pytest
from unittest.mock import patch, mock_open
from my_app.controllers.configuration import ConfigController

@patch('builtins.input', side_effect=['mystorageaccount', 'mycontainer'])
@patch('configparser.ConfigParser.write')
@patch('builtins.open', new_callable=mock_open)
def test_config(mock_file, mock_write, mock_input):
    config_controller = ConfigController()
    config_controller.config()
    
    mock_input.assert_called()
    mock_file.assert_called_with('config.ini', 'w')
    mock_write.assert_called()

