from selenium import webdriver 
import time
from selenium.webdriver.common.by import By
import re
import db

options = webdriver.ChromeOptions()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(options=options)

ORDER_PRICE_PATH = '/html/body/div[1]/div/div[1]/div[4]/div[3]/div[2]/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span'

def save(first, second):
  timestr = time.strftime('%Y.%m.%d' + ' в ' + '%H:%M')

  data_account = open('results.txt', 'a')
  data_account.write(timestr + ' У нас дороже ' + str(first) + ':' + str(second) + '\n')
  data_account.close()


def check_singe_order(browser, order_url, order_path, order_id):
  browser.get(order_url)

  time.sleep(2)
  order_result = browser.find_element(By.XPATH, order_path)
  numeric_part = re.sub(r'[^\d]', '', order_result.text)
  numeric_value = int(numeric_part)

  return order_id, numeric_value


def check_orders():
  browser = webdriver.Chrome('chromedriver')
  orders_list = []

  for sublist  in db.orders:
    order_id = sublist[0]
    for url in sublist[1:3]:
      x = check_singe_order(browser, url, ORDER_PRICE_PATH, order_id)
      orders_list.append(x)

  for i in range(0, len(orders_list), 2):
    if i + 1 < len(orders_list):  
      first = orders_list[i]
      second = orders_list[i + 1]

      if first > second:
        save(first, second)

  print('Результаты сохранены.')

  browser.close()

def main():
  check_orders()

main()