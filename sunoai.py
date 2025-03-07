from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open browser in full screen

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("installed")

# Open Suno AI Website
driver.get("https://suno.com/create")

# Wait for the page to load
time.sleep(5)

print("loaded")


# Find the input field for song generation (Modify XPath based on Suno AI's UI)
try:
    prompt_input = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[1]/div/div[1]/div/div[3]/div[2]/div/div/div[1]/textarea')  
    prompt_input.send_keys("A relaxing Indian classical melody with flute and tabla.")
    print("Yes")
    
    
    # Step 4: Click on "Create" Button
    create_button = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[1]/div/div[1]/div/div[3]/div[4]/button')  # Replace with actual XPath
    create_button.click()
    print("create")

    time.sleep(10)

    print("Entered song prompt and submitted.")

except Exception as e:
    print("Song input field not found. Check the website structure.")

# Wait for song generation
time.sleep(30)  

print("Song should be generated now. Please check the Suno AI interface.")

# Keep browser open for review
time.sleep(10)

# Close browser
driver.quit()
