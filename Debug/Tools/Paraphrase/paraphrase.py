import time
import os
import glob
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

combined_dataset_file = 'Datasets/Primary Datasets/BBC Arabic/FiltBBC.csv'
start_index = 1
end_index = 5000

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://www.paraphrasetool.com/')
combined_df = pd.read_csv(combined_dataset_file)
modified_df = pd.DataFrame(columns=['text', 'psummary'])
download_directory = "C:/Users/youss/Downloads"

try:
    dropdown_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'text_entry_text_entrydropdown_holder')))
    dropdown_button.click()

    diplomatic_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@data-value="diplomatic"]')))
    diplomatic_option.click()
except:
    pass

time.sleep(2)

def Check_Paraphrase_Done(driver, class_name):
    while True:
        try:
            time.sleep(1) 
            element = driver.find_element(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            return True
        
for index, row in tqdm(combined_df[start_index-1:end_index].iterrows(), total=(end_index-start_index+1), desc="Processing"):
    try:
        summary = row['summary']
        text = row['text']

        try:
            sample_text_button = driver.find_element(By.CSS_SELECTOR, 'span#sample_text_helper')
            sample_text_button.click()
        except:
            pass
        
        text_input_field = driver.find_element(By.CSS_SELECTOR, 'textarea#text_entry_entry_text_input')
        text_input_field.clear()
        text_input_field.send_keys(summary)

        paraphrase_button = driver.find_element(By.ID, 'text_entry_paraphrase_submitbuttonParaphrase')
        driver.execute_script("arguments[0].click();", paraphrase_button)
        
        class_name = 'MuiSkeleton-root'
        isPDone = Check_Paraphrase_Done(driver, class_name)
        
        if isPDone:
            download_button = driver.find_element(By.CSS_SELECTOR, 'img.img_dark[alt="download"]')
            download_button.click()

        time.sleep(2) 

        downloaded_files = glob.glob(os.path.join(download_directory, 'ParaphrasedText*.txt'))
        if len(downloaded_files) > 0:
            downloaded_file = downloaded_files[0]

            with open(downloaded_file, 'r', encoding='utf-8') as file:
                downloaded_text = file.read()

            modified_df = modified_df.append({'text': text, 'psummary': downloaded_text}, ignore_index=True)
            os.remove(downloaded_file)
            modified_df.to_csv('Debug/Tools/Paraphrase/Paraphrased Dataset/ModDataset.csv', index=False)
    except:
        print("Error on ", index)
        driver.quit()
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.paraphrasetool.com/')
        summary = row['summary']
        text = row['text']
        
        try:
            dropdown_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'text_entry_text_entrydropdown_holder')))
            dropdown_button.click()

            diplomatic_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@data-value="diplomatic"]')))
            diplomatic_option.click()
        except:
            pass

        time.sleep(2)

        try:
            sample_text_button = driver.find_element(By.CSS_SELECTOR, 'span#sample_text_helper')
            sample_text_button.click()
        except:
            pass
        
        text_input_field = driver.find_element(By.CSS_SELECTOR, 'textarea#text_entry_entry_text_input')
        text_input_field.clear()
        text_input_field.send_keys(summary)

        paraphrase_button = driver.find_element(By.ID, 'text_entry_paraphrase_submitbuttonParaphrase')
        driver.execute_script("arguments[0].click();", paraphrase_button)
        
        class_name = 'MuiSkeleton-root'
        isPDone = Check_Paraphrase_Done(driver, class_name)
        
        if isPDone:
            download_button = driver.find_element(By.CSS_SELECTOR, 'img.img_dark[alt="download"]')
            download_button.click()

        time.sleep(2) 

        downloaded_files = glob.glob(os.path.join(download_directory, 'ParaphrasedText*.txt'))
        if len(downloaded_files) > 0:
            downloaded_file = downloaded_files[0]

            with open(downloaded_file, 'r', encoding='utf-8') as file:
                downloaded_text = file.read()

            modified_df = modified_df.append({'text': text, 'psummary': downloaded_text}, ignore_index=True)
            os.remove(downloaded_file)
            modified_df.to_csv('Debug/Tools/Paraphrase/Paraphrased Dataset/ModDataset.csv', index=False)
