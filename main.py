from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from PIL import ImageGrab
import os


def extract_datee(date_str):
    try:
        date_str = date_str.split(',')[1].split(' ')[1]
        return date_str
    except ValueError:
        print("returnd none")
        return None
    # Specify the directory where you want to save the screenshot
directory = 'screenshots'
def extract_numbers(input_string):
    # Use regular expression to extract numbers
    numbers = re.findall(r'\d+', input_string)
    # Join the extracted numbers into a string
    extracted = ''.join(numbers)
    return extracted
def screenshot(name,directory,date):
    print(name)
    directory = directory +'/'+ extract_datee(str(date))
    # Ensure the directory exists, create it if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Take a screenshot of the entire screen
    screenshot = ImageGrab.grab()
    print(directory)
    # Save the screenshot to the specified directory
    file_path = directory + f"/{name}.png"
    screenshot.save(file_path)
    return file_path

# def sameItem():

def convert_date(input_date):
    # Split the input date into year, month, and day
    year, month, day = input_date.split('-')
    yearsingele = int(year)%10
    yeartho = int(year)/1000*10
    # Format the date in the desired output format
    output_date = f"{day}.{month}.{str(int(yeartho)+int(yearsingele))}"
    return output_date

# Function to extract the date from the website
def extract_date(driver):
    sleep(5)
    date = ''
    try:
        date = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[5]/div[1]/div[2]/div[2]/div/div[1]/div/div/div[4]/div[1]').text
    except NoSuchElementException:
        print("basa")
    return date




def add0 (minute):
    if minute<10:
        minute = '0'+str(minute)
    return minute
# Function to automate button click
count = 1
def click_button_with_date(date, driver,count):
    nowDate = " "+str(add0(datetime.now().time().hour))+':'+str(add0(datetime.now().time().minute))+", "+ str(convert_date(str(datetime.today()).split(' ')[0]))
    date = date.split(",")[2]+','+date.split(",")[1]
    # sleep(1000)
    # nameOfOffice = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[5]/div[1]/div[2]/div[2]/div/div[1]/div/div/div[4]/h2/span').text
    #
    # print(nameOfOffice)
    # nowDate = date #check row for if the button is working
    if date == nowDate:
        original_window = driver.current_window_handle
        # Find and click the button (replace XPATH_OF_THE_BUTTON with the actual XPath of the button)
        button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[5]/div[1]/div[2]/div[2]/div/div[1]/div/div')
        button.click()
        print("Button clicked!")
        count+=1
        wait = WebDriverWait(driver, 10)
        wait.until(EC.number_of_windows_to_be(2))
        # Loop through until we find a new window handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        sleep(6)
        driver.find_element(By.XPATH,'/html/body/div[6]/div[1]').click()
        sleep(1)
        last_name = ''
        name = ' '
        file_path = ""
        flag = True
        lowest_number = 10000000
        while flag:
            try:
                try:
                    while 'מתחילים'in driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[1]/div[3]/div[9]/div[3]').text:
                        sleep(40)
                        print("waiting")
                except NoSuchElementException:
                    print('oops')
                    pass
                # sleep(1000)
                while driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div[4]/div[6]/div[3]/div').text=="אין הצעות" :
                    sleep(1)
                    while driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div[4]/div[6]/div[3]/div').text == "":
                        print("sleeping...")
                        sleep(0.5)
                    sleep(2)
                    try:
                        name = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[1]/div[3]/div[8]/div[2]/div[1]').text
                    except NoSuchElementException:
                        name = "1"

                    number = int(extract_numbers(str(driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div[4]/div[6]/div[2]/div[1]').text)))
                    last_name = name
                    if number<lowest_number:
                        file_path = screenshot(extract_numbers(name),directory,date)
                        print("screenshot taken")
                        lowest_number = number
                    sleep(10)
                if last_name == name:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"File '{file_path}' deleted successfully.")
                    else:
                        sleep(1)

            except NoSuchElementException:
                print("Finished sale")
                flag = False
                driver.close()
                driver.switch_to.window(original_window)
    else:
        print("Date does not match.")

url = 'https://cars.bidspirit.com/ui/home?lang=he'  # Replace with the website URL you want to extract date from
web = webdriver.Chrome()
web.get(url)
# web.maximize_window()
# Extract the date from the website
extracted_date = extract_date(web)

# Perform button click if the extracted date matches a condition
if extracted_date:
    while 1:
        click_button_with_date(extracted_date,web,count)
        sleep(30)
else:
    print("Date not found or extraction failed.")
web.quit()
