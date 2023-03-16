import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint
import pandas as pd

from configparser import ConfigParser
config = ConfigParser()
config.read('/config/key_config.cfg')

USER_NAME = config.get('Linkedin', 'user_name')
PASS_WORD = config.get('Linkedin', 'pass_word')

options = Options()
# options.add_argument('--headless')
# options.add_argument("--incognito")

#public
url = "https://www.linkedin.com/in/hoangtungw/"
#private
# url = "https://www.linkedin.com/in/hung-nguyen-thanh-216424144"
#local 
# url = "file:///Users/ptta/Python/Learning%20Python/TestData/(15)LinkedIn.html"

years = []

chromedriver_autoinstaller.install()


def cal_month_of_exp(input,short_type=False):
    input_str = str(input)
    if short_type:
      regex = r"(.+ yr.?)?(.+ mo.?)?"
    else:
      regex = r"(.+ year.?)?(.+ month.?)?"
    match = re.search(regex, input_str)
    cal_moe = 0
    if (match is not None):
        if 'year' in match.group(0) or 'yr' in match.group(0):
            extract_year = re.search(r'\d+', match.group(0))
            cal_moe += int(extract_year.group(0))*12
        if 'month' in match.group(0) or 'mo' in match.group(0):
            extract_month = re.search(r'\d+', match.group(2))
            cal_moe += int(extract_month.group(0))
    return cal_moe


def num_check(string):
    if len(string)>18:
      return False
    else:
      return True

def web_crawl(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(randint(3,5))
    try:
      public_profile(driver)
    except:
        print(f'Private profile')
        login_linkldin(driver)
        public_profile(driver)


def login_linkldin(driver):
    signin_btn = driver.find_element(By.XPATH,'//*[@id="public_profile_contextual-sign-in"]/div/section/main/div/div/div[1]/button')
    signin_btn.click()
    ### get username and password input boxes path
    username = driver.find_element(By.XPATH,"//input[@name='session_key']")
    password = driver.find_element(By.XPATH,"//input[@name='session_password']") 
    ### input the email id and password
    time.sleep(randint(1,2))
    username.send_keys(USER_NAME)
    time.sleep(randint(2,3))
    password.send_keys(PASS_WORD)
    time.sleep(randint(1,2))
    ### click the login button
    login_btn = driver.find_element(By.XPATH,"//button[@type='submit']")
    login_btn.click()

def public_profile(driver):
    final_result = []
    final_months = 0
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    profile = soup.find("section", class_="profile")
    experiences = profile.find("ul", class_="experience__list")
    current_duration = experiences.find_all(
        "p", class_='experience-group-header__duration')
    for current in current_duration:
        print(current.get_text().strip())
        final_result.append(current.get_text().strip())
    past_working_durations = experiences.find_all(
        "p", class_="experience-item__duration experience-item__meta-item")
    for duration in past_working_durations:
        result = duration.find("span", class_="date-range__duration")
        print(result.get_text())
        final_result.append(result.get_text())
    if len(final_result) > 0:
        for months in final_result:
            final_months += cal_month_of_exp(months)
    years.append(final_months/12)
    print(f'Total year of exp: {final_months/12}')

def private_profile(driver):
    final_result = []
    final_months = 0
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    profiles = soup.find_all("div", class_="display-flex flex-column full-width align-self-center")
    count_company = len(soup.find_all("a", attrs={"data-field":"experience_company_logo"}))
    if count_company > 1:
       count_company -= 1
    print(f"Number of company: {count_company}")
    for profile in profiles:
      experiences = profile.find_all("span", class_="visually-hidden")
      for experience in experiences:
        text = experience.get_text().split(" · ")[-1]
        if ('yr' in text or 'mo' in text) and (num_check(text)):
          print(text)
          print(cal_month_of_exp(text,short_type=True))


def excel_reader():
  dataframe = pd.read_excel('Hanoi List copy.xlsx', sheet_name='Sheet1', usecols='G')
  linklist = []
  for index, row in dataframe.iterrows():
    linklist.append(row[0])
  return linklist

if __name__ == "__main__":
    # urllist = excel_reader()
    # for url in urllist:
    #     print(url)
    #     web_crawl(url)
    # df = pd.DataFrame(years)
    # df.to_csv("output.csv")
    
    # driver = webdriver.Chrome(options=options)
    # driver.get(url)
    # time.sleep(randint(3,5))
    # login_linkldin(driver)
    # time.sleep(randint(1,3))
    # private_profile(driver)

    web_crawl(url)
