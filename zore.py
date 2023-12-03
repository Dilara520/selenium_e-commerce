from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
import os
import pathlib
import urllib.request

search_query = "youngkit 14 pro max"

if not os.path.exists(f"/Users/Dilara/Desktop/{search_query}"):
    os.mkdir(f"/Users/Dilara/Desktop/{search_query}")

browser = webdriver.Chrome()
browser.get(f"https://www.zoreaksesuar.com/arama?q={search_query}") # any e-commerce page with infinite scroll
browser.implicitly_wait(3)

products = browser.find_elements(By.CSS_SELECTOR, "#catalog886 > div") # element selector paths are specific to the selected page
# print(len(products), totalProd) for comparison to make sure

# scroll to the end of the search result page (infinite scroll) then turn back to the beginning for automation process
if (len(products) >= 64): #there is 64 product listed before other part of the page loads
    scrolls = len(products) // 64

    for i in range(scrolls):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

for i in range(len(products)):
    browser.execute_script("arguments[0].scrollIntoView();", products[i])
    time.sleep(2)
    clickp = products[i].find_element(By.CSS_SELECTOR, "div > div.col-12.py-1.product-detail-card.height-equalized > div > div:nth-child(1) > a")
    # navigate to product page - and wait for the page to be loaded
    clickp.click()
    time.sleep(3)

    product_name = browser.find_element(By.CSS_SELECTOR, "#product-title").text

    # folder created with the name of search_query
    folder_path = f"/Users/Dilara/Desktop/{search_query}/{product_name}"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # each product has its own folder and its images saved
    images = browser.find_elements(By.CSS_SELECTOR,"#product-left > div > div.w-100.position-relative.product-images-thumb > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events.swiper-container-thumbs > div.swiper-wrapper > div")
    for i, image in enumerate(images):
        imgK = image.find_element(By.CSS_SELECTOR,"div > figure > img").get_attribute("src")
        imgB = imgK.replace("-K.jpg", "-B.jpg")
        # save big version of each image
        screenshot_path = f"{folder_path}/{i+1}.jpg"
        urllib.request.urlretrieve(imgB, screenshot_path)
    
    browser.back()
    time.sleep(2)
    products = browser.find_elements(By.CSS_SELECTOR, "#catalog886 > div") # element id changes each time page reloads

browser.quit()