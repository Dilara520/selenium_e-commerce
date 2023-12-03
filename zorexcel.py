from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
import pandas as pd

search = "youngkit 12 pro"

browser = webdriver.Chrome()
browser.get(f"https://www.zoreaksesuar.com/arama?q={search}")
browser.implicitly_wait(3)

products = browser.find_elements(By.CSS_SELECTOR, "#catalog886 > div")

if (len(products) >= 64):
    scrolls = len(products) // 64

    for i in range(scrolls):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

data = []

for i in range(len(products)):
    browser.execute_script("arguments[0].scrollIntoView();", products[i])
    time.sleep(2)
    clickp = products[i].find_element(By.CSS_SELECTOR, "div > div.col-12.py-1.product-detail-card.height-equalized > div > div:nth-child(1) > a")
    clickp.click()
    time.sleep(3)

    product_name = browser.find_element(By.CSS_SELECTOR, "#product-title").text
    barcode = browser.find_element(By.CSS_SELECTOR, "#barcode-product-code").text
    model_code = browser.find_element(By.CSS_SELECTOR, "#supplier-product-code").text #with T
    stock_code = model_code[1:] #without T
    aciklama = browser.find_element(By.CSS_SELECTOR, "#product-fullbody > div:nth-child(1)").text

    colors_list = [] #B P
    colors = browser.find_elements(By.CSS_SELECTOR, "#product-right > div.w-100.position-relative.popover-wrapper > div.w-100.variant-wrapper > div > div > div.w-100.sub-one > div > a")
    for j in range(len(colors)):
        color_text = colors[j].find_element(By.CSS_SELECTOR, "figure > span").text
        if color_text[0] not in colors_list: # when it comes to the color Blue, the first two letters of the color will be added to the end of the stock_code since the letter B (Brown) is already in the list (else condition).
            colors_list.append(color_text[0])
            modified_stock_code = stock_code + color_text[0] #57438B
        else:
            modified_stock_code = stock_code + color_text[:2] #57438Bl

        colors[j].click()
        barcode_c = browser.find_element(By.CSS_SELECTOR, "#barcode-product-code").text
        modified_product_name = product_name + " " + color_text
        
        color_info = [model_code, modified_stock_code, "", barcode_c, barcode_c, modified_product_name, aciklama]
        data.append(color_info)
    
    browser.back()
    time.sleep(2)
    products = browser.find_elements(By.CSS_SELECTOR, "#catalog886 > div")

browser.quit()

df = pd.DataFrame(data, columns=["ModelKodu", "StokKodu", "VaryasyonStokKodu", "Barkod", "VaryasyonBarkod", "UrunAdi", "Aciklama"])
search_query = search.replace(" ", "_")
file_name = f"/Users/Dilara/Desktop/{search_query}.xlsx"
df.to_excel(file_name, index=False) # at the end, an excel folder created in the spefied path with the given name - columns and rows are written
