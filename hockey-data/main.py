import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

url = "https://www.scrapethissite.com/pages/forms/"

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
driver.get(url)
headers = []
data = []

print("scraping data")
while True:
    soup = BeautifulSoup(driver.page_source, 'lxml')
    if not headers:
        headerrow = soup.select_one("tr")
        headers = [th.text.strip() for th in headerrow.select("th")]
    for team in soup.select(".team"):
        cells = team.find_all("td")
        rowdata = {}
        for i in range(len(headers)):
            value = cells[i].text.strip() if i < len(cells) and cells[i].text.strip() else ""
            rowdata[headers[i]] = value
        data.append(rowdata)
    try:
        driver.find_element(By.XPATH, '//a[@aria-label="Next"]').click()
    except NoSuchElementException or ElementNotInteractableException:
        print("done scraping data")
        break
with open("hockey.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
    print("data saved to file")

driver.quit()
