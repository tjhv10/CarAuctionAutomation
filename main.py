import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import openpyxl
from openpyxl import load_workbook

# Path to the Excel file
excel_file = "car_data.xlsx"

# Check if the file exists
if os.path.exists(excel_file):
    # Load the workbook and select the active worksheet
    wb = load_workbook(excel_file)
    ws = wb.active
else:
    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Car Data"
    # Add headers to the Excel sheet
    headers = ["Link", "Name", "Description"]
    ws.append(headers)

# URL of the website to scrape
url = 'https://cars.bidspirit.com/ui/home?lang=he'

# Initialize the WebDriver
web = webdriver.Chrome()
web.get(url)
sleep(3)

# Reject cookies
web.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]').click()

for i in range(1, 20):
    sleep(2)
    web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div[2]/div/div[5]/div[1]/div[2]/div[2]/div/div[' + str(i) + ']/div/div').click()
    sleep(3)
    try:
        num_of_cars = int(web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div').text.split(' ')[0])
    except NoSuchElementException:
        num_of_cars = 0
    
    for j in range(1, num_of_cars + 1):
        link = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[' + str(j) + ']/div[1]/div/div/div[3]/div[3]/div[1]/a').get_attribute('href')
        web.get(link)
        sleep(3)
        name = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h1').text
        disc = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h2').text
        # Add data to Excel sheet
        ws.append([link, name, disc])
        web.back()
    
    if num_of_cars == 0:
        link = web.current_url
        name = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h1').text
        disc = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h2').text
        # Add data to Excel sheet
        ws.append([link, name, disc])
    
    web.back()

# Save the workbook
wb.save(excel_file)

# Close the browser
web.quit()
