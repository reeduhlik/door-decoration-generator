from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def make_image(driver, first, last):


    #Set the textarea element with id tt-text-textarea to be "TEST NAME"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'tt-text-textarea')))

    #Wait for the element to be interactable
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'tt-text-textarea')))
    #Clear the text area
    driver.find_element(By.ID, "tt-text-textarea").clear()

    #Send the first and last name to the textarea
    if last == "X":
        driver.find_element(By.ID, "tt-text-textarea").send_keys(f"{first}")
    else:
        driver.find_element(By.ID, "tt-text-textarea").send_keys(f"{first} {last}.")

    ##Click on the element with the attribute data-name=save
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-name="save"]')))
    driver.find_element(By.CSS_SELECTOR, '[data-name="save"]').click()

    #Inside the ul with id tt-download-format-list, click on the second li
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'tt-download-format-list')))

    #Click on the button inside of the second li
    driver.find_element(By.ID, "tt-download-format-list").find_elements(By.TAG_NAME, "li")[1].click()


    #Inside the div with id tt-download-popup, click on the button with a class tt-download-button
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'tt-download-popup')))

    #Wait for the button to be clickable
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'tt-download-button')))
    driver.find_element(By.ID, "tt-download-popup").find_element(By.CLASS_NAME, "tt-download-button").click()

    #Click on the div with class tt-clsoe
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'tt-close')))

    #Make sure the element is clickable
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'tt-close')))
    driver.find_element(By.CLASS_NAME, "tt-close").click()


    ##Click on the element with the attribute data-name=save
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-name="text"]')))
    driver.find_element(By.CSS_SELECTOR, '[data-name="text"]').click()


    

def main():
    #Setup the driver
    # Initialize selenium used to scrape the website
    options = webdriver.ChromeOptions()
    # options.headless = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version="127.0.6533.120").install()), options=options)

    #Wait 3 seconds for the page to load
    driver.get("https://www.textstudio.com/logo/super-mario-599")

    #Open the csv file test.csv
    with open("./names.csv", "r") as file:
        #The file contains first_name, last_name
        #Read the first name and first character of the last name
        for line in file:
            first_name, last_name = line.strip().split(",")
            last_name = last_name[0]
            #Make the image
            make_image(driver, first_name, last_name)



    #CLose on input


if __name__ == "__main__":
    main()