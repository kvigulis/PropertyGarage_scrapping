from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import tqdm

from scrapping.models import ResultProperty

from django.utils import timezone

import time
from django.conf import settings
from os.path import join as pjoin

def scap_rightmove(url):
    current_date = timezone.now()
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(pjoin(settings.BASE_DIR,"chromedriver"), chrome_options=options)

    driver.implicitly_wait(25)

    current_url = url

    driver.get(current_url)

    pagination_dropdown = driver.find_elements_by_class_name('pagination-dropdown')[0]
    last_page = int(pagination_dropdown.find_elements_by_tag_name('option')[-1].get_attribute('innerHTML'))

    print("last_page:", last_page)

    BINGO_results_URLs = []
    BINGO_results_IDs = []

    for page in tqdm.tqdm(range(1, last_page + 1)):

        print("========== PAGE:", page)
        print("current_url :::", current_url)
        # loads a webpage from an url and returns two WebElement lists to iterate through: one with titles and other with prices
        resultsItems = driver.find_elements_by_class_name('l-searchResult')

        print("Number of results:", len(resultsItems))
        property_links = []
        property_ids = []
        for result in resultsItems:
            link_div_list = result.find_elements_by_class_name('propertyCard-link')
            property_id = result.get_attribute('id').split('-')[-1]
            #print("property_id:", property_id)
            if len(link_div_list) > 0:
                link_URL = link_div_list[0].get_attribute('href')
                #print(link_URL)
                property_links.append(link_URL)
                property_ids.append(property_id)

        for link_URL, property_ID in tqdm.tqdm(zip(property_links, property_ids), total=len(property_links)):
            #print("\n\n======= Opening result: ", link_URL, "=============")
            driver.get(link_URL)
            title = driver.find_elements_by_tag_name('title')[0].get_attribute('innerHTML')
            price_div = driver.find_elements_by_class_name('property-header-price')[0]
            price_text = price_div.find_elements_by_tag_name('strong')[0].get_attribute('innerHTML').split('<')[0]
            descriptions = driver.find_elements_by_class_name('sect')
            whole_text = ""
            for sect in descriptions:
                whole_text += sect.text
            if 'garage' in whole_text.lower():
                try:
                    ResultProperty.objects.get(property_id=property_ID)
                    print("Property already exists:", link_URL)
                except:
                    result_obj = ResultProperty()
                    result_obj.date = current_date
                    result_obj.price = price_text
                    result_obj.title = title
                    result_obj.URL = link_URL
                    result_obj.property_id = property_ID
                    result_obj.save()
                    BINGO_results_URLs.append(link_URL)
                    print("New property added:", link_URL)
                continue
            if ' shed ' in whole_text.lower():
                try:
                    ResultProperty.objects.get(property_id=property_ID)
                    print("Property already exists:", link_URL)
                except:
                    result_obj = ResultProperty()
                    result_obj.date = current_date
                    result_obj.price = price_text
                    result_obj.title = title
                    result_obj.URL = link_URL
                    result_obj.property_id = property_ID
                    result_obj.save()
                    BINGO_results_URLs.append(link_URL)
                    print("New property added:", link_URL)
                continue

        driver.get(current_url)

        print("Current Matching results:", BINGO_results_URLs)
        try:
            next_page_btn = driver.find_elements_by_class_name('pagination-direction--next')[0]
            print("next_page_btn", next_page_btn.get_attribute('innerHTML'))
            next_page_btn.send_keys(Keys.END)
            next_page_btn.send_keys(Keys.END)
        except:
            break
        print(next_page_btn.text)
        # go to next page
        webdriver.ActionChains(driver).move_to_element_with_offset(next_page_btn, 5, 5).perform()
        next_page_btn.click()
        time.sleep(1)
        current_url = driver.current_url




    print("======= Matches: =======")
    for match_URL in BINGO_results_URLs:
        print("Found match:", match_URL)
