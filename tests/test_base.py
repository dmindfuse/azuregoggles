import pytest
from my_app.controllers.base import BaseController

def test_base_controller():
    base_controller = BaseController()
    assert isinstance(base_controller, BaseController)

if __name__ == '__main__':
    pytest.main()

