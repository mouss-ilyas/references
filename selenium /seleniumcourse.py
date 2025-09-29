from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
time.sleep(4)
driver = webdriver.Firefox()
driver.get("https://example.com/login")

try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password = driver.find_element(By.ID, "password")
    submit = driver.find_element(By.ID, "submit")

    username.send_keys("your_username")
    password.send_keys("your_password")
    submit.click()

    c=username.get_attribute("value")
    print("Login successful! Page title:", driver.title,c)
    driver.save_screenshot("screenshot.png")

finally:
    driver.quit()

################################
alert = driver.switch_to.alert
alert.accept()
alert.dismiss()
alert_text = alert.text
print(alert_text)
#################################

# Get the main window handle
main_window = driver.current_window_handle

# Click a link that opens a new window
driver.find_element(By.LINK_TEXT, "Open New Window").click()

# Get all window handles
all_windows = driver.window_handles

# Switch to the new window
new_window = [window for window in all_windows if window != main_window][0]
driver.switch_to.window(new_window)

# Perform actions in the new window
print("New window title:", driver.title)

# Close the new window
driver.close()

# Switch back to the main window
driver.switch_to.window(main_window)
#############################################