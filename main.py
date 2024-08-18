import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import openpyxl
from openpyxl import load_workbook
excel_file = "car_data.xlsx"
if os.path.exists(excel_file):
    wb = load_workbook(excel_file)
    ws = wb.active
else:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Car Data"
    headers = ["loyer" ,"link", "name", "disc", "hand","picture"]
    ws.append(headers)

url = 'https://cars.bidspirit.com/ui/home?lang=he'

web = webdriver.Chrome()
web.get(url)
sleep(3)
web.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]').click()

for i in range(7, 8):
    sleep(2)
    web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div[2]/div/div[5]/div[1]/div[2]/div[2]/div/div[' + str(i) + ']/div/div').click()
    sleep(3)
    try:
        num_of_cars = int(web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div').text.split(' ')[0])
    except NoSuchElementException:
        num_of_cars = 0
    j = 1
    for k in range(1, num_of_cars + 1):
        loy = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[2]/h2/a').text
        print(loy,"jhfhg")
        try:
            sleep(3)
            web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div['+str(j)+']/div[1]').click()
        except NoSuchElementException:
            sleep(3)
            web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/a[7]').click()
            sleep(3)
            j = 1
            web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div['+str(j)+']/div[1]/div').click()
        j += 1
        sleep(3)
        l = 1
        web.find_element(By.XPATH,'//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[8]/div[1]/div/img').click()
        sleep(3)
        # pic = [3]
        # for i in range(0,3):
        pic = web.find_element(By.XPATH,'//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div/img').get_attribute('src')
        # web.find_element(By.XPATH,'//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[3]').click()
        sleep(1)
        print(pic)
        web.back()
        sleep(3)
        try:
            while web.find_element(By.XPATH,'//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[11]/table/tbody/tr['+str(l)+']/th').text != "יד":
                l+=1
            hand = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[11]/table/tbody/tr['+str(l)+']/td').text
        except:
            pass
        try:
            link = web.current_url
            name = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h1').text
            disc = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h2').text
            ws.append([loy,link, name, disc, hand,pic])
        except NoSuchElementException:
            pass    
        web.back()
    
    if num_of_cars == 0:
        try: 
            loy = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[2]/h2/a').text
        except:
            loy = "None"
        try:
            while web.find_element(By.XPATH,'//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[11]/table/tbody/tr['+str(l)+']/th').text != "יד":
                l+=1
            hand = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[11]/table/tbody/tr['+str(l)+']/td').text
        except:
            pass
        link = web.current_url
        try:
            name = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h1').text
            disc = web.find_element(By.XPATH, '//*[@id="mainView"]/div/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[5]/h2').text
            ws.append([loy ,link, name, disc, hand,pic])
        except NoSuchElementException:
            pass
    web.back()

wb.save(excel_file)
web.quit()
