from dataclasses import dataclass

@dataclass
class LoginData:
    username: str
    password: str
    expected_message: str

valid_data = LoginData(username="admin", password="admin123", expected_message="reset password link sent successfully")
invalid_data = LoginData(username="invalid_user", password="invalid_pass", expected_message="Invalid credentials")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.mark.parametrize("data", [valid_data])
def test_forgot_password_link(data: LoginData):
    driver = webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Click on "Forgot password" link
    forgot_password_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Forgot password?"))
    )
    forgot_password_link.click()

    # Verify username field is visible
    username_field = driver.find_element(By.ID, "username")
    assert username_field.is_displayed()

    # Enter username and submit
    username_field.send_keys(data.username)
    driver.find_element(By.ID, "resetBtn").click()

    # Verify success message
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "auth-form-message"))
    )
    assert success_message.text == data.expected_message

    driver.quit()