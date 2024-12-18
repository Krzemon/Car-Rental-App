import pytest
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow

@pytest.fixture(scope="module")
def app():
    return QApplication([])

def test_login_window_initialization(app):
    login_window = LoginWindow()
    assert login_window.windowTitle() == "Car Rental System - Login"

def test_login_valid_credentials(mocker, app):
    login_window = LoginWindow()
    mocker.patch("gui.login_window.USER_DATABASE", {
        "admin": {"password": "admin123", "role": "Administrator"}
    })

    login_window.username_input.setText("admin")
    login_window.password_input.setText("admin123")

    spy = mocker.spy(login_window, "open_main_window")
    login_window.authenticate_user()

    spy.assert_called_once_with("Administrator")
