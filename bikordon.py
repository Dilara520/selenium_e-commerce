from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
import os
import pathlib
import urllib.request

search_query = "youngkit 14 pro max siyah"

if not os.path.exists(f"/Users/Dilara/Desktop/{search_query}"):
    os.mkdir(f"/Users/Dilara/Desktop/{search_query}")

browser = webdriver.Chrome()
browser.get(f"https://www.bikordon.com/search?type=product&q={search_query}")
browser.implicitly_wait(3)

products = browser.find_elements(By.CSS_SELECTOR, "body > div.page-content > div.container > div.row.row-flex > div > div > div.prd-grid.data-to-show-4.data-to-show-md-4.data-to-show-sm-2.js-category-grid.product-listing.prd-text-center > div")

while(True):
    for k in range(len(products)):
        browser.execute_script("arguments[0].scrollIntoView();", products[k])
        time.sleep(2)
        clickProduct = products[k].find_element(By.CSS_SELECTOR, "div > div.prd-info > h2 > a")
        # click on the product to navigate to its page
        clickProduct.click()
        time.sleep(3)

        product_name_error = browser.find_element(By.CSS_SELECTOR, "#prdGallery100 > div.col-md > div > div > div > div.prd-block_title-wrap > h1").text
        product_name = product_name_error.replace("/", "_")

        folder_path = f"/Users/Dilara/Desktop/{search_query}/{product_name}"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        
        gallery = browser.find_element(By.CSS_SELECTOR, "#prdGallery100 > div.col-md-6.col-xl-5 > div.product-previews-wrapper.always-visible > div")
        galleryId = gallery.get_attribute("id")
        # find and save product images
        images = gallery.find_elements(By.CSS_SELECTOR, "div > div > a")

        for i, image in enumerate(images):
            img = None
            data_image = image.get_attribute("data-image")
            data_video = image.get_attribute("data-video")

            if data_image:
                img = data_image.replace("//www.", "https://www.")
            elif data_video:
                img = data_video

            if img:
                # save each image/video in big size
                file_extension = 'jpg' if data_image else 'mp4' # considering both img and video
                screenshot_path = f"{folder_path}/{i+1}.{file_extension}"
                urllib.request.urlretrieve(img, screenshot_path)

        browser.back()
        time.sleep(2)

    # find all the page navigation elements
    page_navigation = browser.find_elements(By.CSS_SELECTOR, "body > div.page-content > div.container > div.row.row-flex > div > div > div.d-flex.mt-4.mt-md-6.justify-content-center.align-items-start > ul > li")
    next_button_title = page_navigation[len(page_navigation)-1].find_element(By.CSS_SELECTOR, "a").get_attribute("title")

    # pages structure at the end instead of infinite scroll in this example of e-commerce
    if next_button_title == "Sonraki »":
        next_button = page_navigation[len(page_navigation)-1].find_element(By.CSS_SELECTOR, "a")
        next_button.click()
        time.sleep(3)
        products = browser.find_elements(By.CSS_SELECTOR, "body > div.page-content > div.container > div.row.row-flex > div > div > div.prd-grid.data-to-show-4.data-to-show-md-4.data-to-show-sm-2.js-category-grid.product-listing.prd-text-center > div")
    else:
        break  # break the loop if there's no "Next" button (end)

browser.quit()
