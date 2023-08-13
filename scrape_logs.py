import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import warnings

def scrape_wlogs(doc):
    if doc.get('Level', 0) < 80 or doc.get('Guilde') == '':
        return
    
    url = f"https://classic.warcraftlogs.com/character/eu/{doc['Serveur']}/{doc['Nom du joueur']}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode to avoid opening a browser window
    chrome_options.add_argument("--log-level=3")  # Set log level to ERROR to suppress non-error logs
    driver = webdriver.Chrome(options=chrome_options)

    try:
        with warnings.catch_warnings():  # Suppress warnings from the driver
            warnings.simplefilter("ignore")
            driver.get(url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            span_with_class = soup.find('span', class_='all-stars-rank')
            if span_with_class:
                img_tag = span_with_class.find_next('img')
                if img_tag and 'alt' in img_tag.attrs:
                    doc['Main_spe'] = img_tag['alt']
                else:
                    doc['Main_spe'] = ""
            else:
                doc['Main_spe'] = ""

            div_with_class = soup.find('div', class_='best-perf-avg')
            if div_with_class:
                first_b_tag = div_with_class.find_next('b')
                if first_b_tag:
                    doc['lvl_spe'] = float(first_b_tag.text.strip())
                else:
                    doc['lvl_spe'] = 0
            else:
                doc['lvl_spe'] = 0

    finally:
        driver.quit()
    print(doc)

def get_wlogs(dict_arr):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape_wlogs, dict_arr)
    #for doc in dict_arr:
    #    scrape_wlogs(doc)
    #    print(doc)