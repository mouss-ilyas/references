from selenium import webdriver


driver = webdriver.Firefox()
driver.get("https://khanacademy.com")

# Open a new tab using JavaScript
driver.execute_script("window.open('');")

# Get all window handles
all_tabs = driver.window_handles

# Switch to the new tab
new_tab = all_tabs[1]
driver.switch_to.window(new_tab)

# Navigate to a new URL in the new tab
driver.get("https://example.com/newpage")

# Switch back to the first tab
driver.switch_to.window(all_tabs[0])

driver.quit()
