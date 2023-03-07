import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
from random import randint

options = Options()
options.add_argument('--headless')

url = "https://www.linkedin.com/in/hoangtungw/"

chromedriver_autoinstaller.install()

def cal_month_of_exp(input):
    input_str = str(input)
    regex = r"(.+ year.?)?(.+ month.?)?"
    match = re.search(regex, input_str)
    cal_moe = 0
    if (match != None):
        if 'year' in match.group(0):
            extract_year = re.search(r'\d+', match.group(0))
            cal_moe += int(extract_year.group(0))*12
        if 'month' in match.group(0):
            extract_month = re.search(r'\d+', match.group(2))
            cal_moe += int(extract_month.group(0))
    return cal_moe

def web_crawl(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(randint(2,5))
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
    print(f'Total year of exp: {final_months/12}')


if __name__ == "__main__":
    web_crawl(url)
