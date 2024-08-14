# https://www.youtube.com/watch?v=0CI3Z2kX5c0
# https://www.youtube.com/watch?v=NBuED2PivbY&t=239s
# https://www.youtube.com/watch?v=USrjHgO9Niw&t=25s
# https://www.youtube.com/watch?v=LXRx6FgiiEc&t=799s

# Try doing everything in one tab


import urllib.request
import undetected_chromedriver as uc
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import requests
import random

# This ensures that the images are in the correct order
number = 0

# Sure fire way to close chrome
def kill_chrome():

    try:
        
        # This will terminate all Chrome processes
        os.system(f"taskkill /f /im chrome.exe")

    except Exception as e:
        
        print("Error killing Chrome processes: ", e)

# lead is what we want to search
def get_images(lead):

    global number

    # Options
    options = webdriver.ChromeOptions()

    # Allows for use of my user in chrome tab
    # options.add_argument("--user-data-dir=C:\\Users\\blacb\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

    # Doesn't need to render User Interface

    # options.add_argument("--headless")

    # Windows optimisation
    options.add_argument("--disable-gpu")

    # Disables extensions to prevent extra loading
    options.add_argument("--disable-extensions")
    #options.add_argument("--blink-settings=imagesEnabled=false")

    # Remove unnecessary resources in the chrome tab
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    # Chrome driver launched with minimal overhead
    #options.add_argument("--log-level=3")

    # Adds all the options to undetectable chrome
    driver = uc.Chrome(options=options)

    try:
        # Parameters for google images search
        params = {

            "q": lead,
            "tbm": "isch"
        }

        html = requests.get("https://www.google.com/search", params=params, timeout=30)

        # Opens the url for the image search
        driver.get(html.url)

        try:
            # This finds the reject cookies button on screen and presses it
            rejectCookieButton = driver.find_element(By.ID, "W0wltc")
            rejectCookieButton.click()
        
        except:
            
            driver.quit()
            return get_images(lead)

        # Makes it so that the driver waits at least 10 seconds for a task to execute
        wait = WebDriverWait(driver, 10)

        # Finds all the images on the page with the class specified
        image_results = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//img[@class='YQ4gaf']"))
        )

        # Allows for random image selection so that the same image for the same word has less chance of appearing
        image_number = random.randint(3, len(image_results) - 5)

        # Click on the selected image thumbnail to load the full-size image
        selected_image = image_results[image_number]
        selected_image.click()

        try:
            # Wait for the full-size image to load
            full_image = wait.until(
                EC.presence_of_element_located((By.XPATH, "//img[@class='sFlh5c FyHeAf iPVvYb' and @src and contains(@src, 'http')]"))
            )
        
        except:
            driver.quit()
            return get_images(lead)

        # Get the full-size image URL
        image_url = full_image.get_attribute("src")

        # Folder path to downloaded images
        folder_path = "C:\\Users\\blacb\\Desktop\\webImages\\"

        try:

            # Download image
            urllib.request.urlretrieve(str(image_url), folder_path + f"{number}_{lead}.jpg")
            number += 1

        except:
            driver.quit()
            return get_images(lead)
    
    finally:
        driver.quit()

        kill_chrome()
    

    # debug
    print("you are here")

    return

