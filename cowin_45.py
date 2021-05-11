#! python3
# cowin.py - monitoring cowin for availability of slots

# importing the required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from bs4 import BeautifulSoup
import requests
import time

chrome_options = Options()
chrome_options.add_experimental_option('detach',True)
driver = webdriver.Chrome(options = chrome_options)
url = 'https://www.cowin.gov.in/home'
flag = False

try:
    while True:
        try:
            count = 0
            iter = 0
            while count == 0:
                driver.get(url)

                # searching by district
                driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div/label/div').click()
                time.sleep(0.75)

                # selecting state
                driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[1]/mat-form-field/div/div[1]/div/mat-select/div/div[2]/div').click()
                time.sleep(0.75)

                # selecting maharashtra
                driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/mat-option[22]').click()
                time.sleep(0.75)

                # selecting district
                driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[2]/mat-form-field/div/div[1]/div/mat-select/div/div[2]/div').click()
                time.sleep(0.75)

                if iter == 0:
                    # selecting mumbai
                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/mat-option[17]').click()
                    time.sleep(0.75)
                else:
                    # selecting thane
                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/mat-option[32]').click()
                    time.sleep(0.75)

                # selecting search
                driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[3]/button').click()
                time.sleep(0.75)

                # selecting 45+ age group
                driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[3]/div/div[2]/label').click()

                # selecting 18+ age group
                #driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[3]/div/div[1]/label').click()

                # selecting covidshield
                #driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[3]/div/div[3]/label').click()

                response = driver.page_source
                soup = BeautifulSoup(response,'lxml')
                items = soup.find_all('div',class_ = 'row ng-star-inserted')
                centreNames = soup.find_all('h5',class_ = 'center-name-title')
                for item in items:
                    itemNames = item.find_all('a')
                    for itemName in itemNames:
                        answer = itemName.text.strip('\n').replace(" ", "")
                        if answer.isdigit():
                            print(centreNames[items.index(item)].text.strip(" "),': ',answer,' ','Thane' if iter == 1 else 'Mumbai',' 45')
                            count += 1
                iter = 1 if iter == 0 else 0
                if int(str(time.ctime()).split(':')[1].split(':')[0])%5 == 0 and flag == False:
                    driver.close()
                    driver = webdriver.Chrome(options = chrome_options)
                    flag = True
                elif int(str(time.ctime()).split(':')[1].split(':')[0])%5 != 0 and flag == True:
                    flag = False
            if count > 0:
                import winsound
                duration = 60000 # milliseconds
                freq = 440  # Hz
                winsound.Beep(freq,duration)
            driver.close()
        except exceptions.NoSuchElementException:
            continue

except KeyboardInterrupt:
    # Handling CTRL-C input from the user
    print('\nDone.')