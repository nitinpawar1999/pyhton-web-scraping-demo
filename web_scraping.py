from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from bs4 import BeautifulSoup

import pandas as pd

chrome_executable = Service(
    executable_path='C:\chromeDriver\chromedriver.exe', log_path='NUL')

options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options ,service=chrome_executable)

url = 'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaGyIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Aufz9JgGwAIB0gIkMzZmZTZkNDMtYjA2Yy00NmZhLWI2MzgtNGJhZmE4NDc0YTY42AIF4AIB&sid=39f2dc3fb501081b0d2e6154e8a489c0&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaGyIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Aufz9JgGwAIB0gIkMzZmZTZkNDMtYjA2Yy00NmZhLWI2MzgtNGJhZmE4NDc0YTY42AIF4AIB%26sid%3D39f2dc3fb501081b0d2e6154e8a489c0%26sb_price_type%3Dtotal%26%26&ss=New+Delhi&is_ski_area=0&ssne=New+Delhi&ssne_untouched=New+Delhi&dest_id=-2106102&dest_type=city&checkin_year=2022&checkin_month=10&checkin_monthday=1&checkout_year=2022&checkout_month=10&checkout_monthday=2&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1'

driver.get(url)
hotel_data = []

while True:
    try:
        page = driver.execute_script('return document.body.innerHTML')
        soup = BeautifulSoup(''.join(page), 'html.parser')

        lists = soup.find_all('div', class_='b978843432')

        for list in lists:
            title = list.find('div', class_='fcab3ed991 a23c043802')
            rating = list.find('div', class_='b5cd09854e d10a6220b4')
            room_type = list.find('span', class_='df597226dd')
            price = list.find('span', class_='fcab3ed991 bd73d13072')
            
            if title is None:
                title = ''
            else:
                title = title.text
            
            if rating is None:
                rating = ''
            else:
                rating = rating.text

            if room_type is None:
                room_type = ''
            else:
                room_type = room_type.text

            if price is None:
                price = ''
            else:
                price = price.text[2:].replace(',','')

            data = [title, rating, room_type, price]
            print(data)
            hotel_data.append(data)
            
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[2]/nav/div/div[3]/button'))))
        button = driver.find_element(By.XPATH, '//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[2]/nav/div/div[3]/button')
        button.click()
    except (TimeoutException, WebDriverException) as e:
        print("Last page reached")
        break

df = pd.DataFrame(hotel_data, columns=['title', 'rating', 'room_type', 'price'])

df.to_csv('temp.csv', index=False)

driver.quit()


