from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MCon
import pyperclip
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

keyboard = Controller()
mouse = MCon()

string = 'ndfHFb-c4YZDc-HiaYvf-RJLb9c'
driver = webdriver.Firefox()

def getURL(page):
    URL = None
    driver.get(page)
    try:
        pageObject = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CLASS_NAME, string)))
        URL = pageObject.get_attribute('src')
        ID = driver.title
        saveURL(ID, URL)
    except TimeoutException:
        print('TimeoutException! Retrying {page}'.format(page=page))
        getURL(page)

def saveURL(titleID, url):
    with open('output.txt', 'a') as file:
        file.write(titleID)
        file.write(', ')
        file.write(url)
        file.write('\n')


def main():
    relation = open("relation.txt", "r")
    relation = relation.readlines()
    startpos = 8962    # find line in relation.txt that has the TitleID of the last result in output.txt and start from there
    for i in range(len(relation)-startpos):
        # print(relation[i+startpos])
        print(i+startpos)
        quote_page = relation[i+startpos].split(',')
        getURL(quote_page[1])  # pass URL only


if __name__ == '__main__':
    main()
