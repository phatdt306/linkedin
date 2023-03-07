from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

# options = Options()
# options.headless = True

url="https://www.linkedin.com/in/hoangtungw/"
# url= "file:///Users/ptta/Python/Learning%20Python/Linkdln/LinkedIn.html"

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

def cal_month_of_exp(input):
  input_str = str(input)
  regex = r"(.+ year.?)?(.+ month.?)?"
  match = re.search(regex, input_str)
  cal_moe = 0
  if (match != None):
    if 'year' in match.group(0):
      extract_year = re.search(r'\d+',match.group(0))
      cal_moe += int(extract_year.group(0))*12
    if 'month' in match.group(0):
      extract_month = re.search(r'\d+',match.group(2))
      cal_moe += int(extract_month.group(0))
  return cal_moe

def web_crawl(url):
  driver = webdriver.Chrome()
  driver.get(url)
  html = driver.page_source
  soup = BeautifulSoup(html,'html.parser')
  profile = soup.find("section", class_ ="profile")
  experiences = profile.find("ul", class_ ="experience__list")
  # find_class = "core-section-container__content break-words"
  # experiences = profile.find_all("div", class_ = find_class)
  # profile = soup.find_all("experience")
  f = open("output.txt", "w")
  print(profile.get_text(), file=f)
  f.close()
  current_duration = experiences.find_all("p", class_ ='experience-group-header__duration')
  print(current_duration.get_text().strip())
  past_working_durations = experiences.find_all("p", class_ ="experience-item__duration experience-item__meta-item")
  for duration in past_working_durations:
    result = duration.find("span", class_ ="date-range__duration")
    print(result.get_text())
  
if __name__ == "__main__":
  web_crawl(url)

