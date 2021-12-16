import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored



options = Options()
options.add_argument("--headless")

tech = str(sys.argv[1])
safe_mode = str(sys.argv[2])

countries = ['Argentina', 'Armenia', 'Australia', 'Austria', 'Bangladesh', 'Belarus', 'Belgium', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus', 'Chequia', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Hong Kong', 'Hungary', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kazakhstan', "Corea del Sur", 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Malaysia', 'Mexico', 'Moldova', 'Montenegro', 'Morocco', 'Nepal', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Rusia', 'San Marino', 'Saudi Arabia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam']
countries_json = {}
driver = webdriver.Firefox(firefox_options=options)
errors = []

for country in countries:
    link = "https://www.linkedin.com/jobs/search?keywords={}&location={}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0".format(tech, country)
    
    driver.get(link)
    try:
        if safe_mode == '--safe':
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results-context-header__job-count"))
            )
        else:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results-context-header__job-count"))
            )
    except:
        pass

    total_jobs_count = driver.find_elements_by_class_name('results-context-header__job-count')
    
    try:
        result = total_jobs_count[0].get_attribute('innerHTML').replace('+', '').replace(',','')
        countries_json[country] = result
        if int(result) > 12000:
            print('{}: '.format(country) + colored('{}'.format(total_jobs_count[0].get_attribute('innerHTML')), 'green'))
        elif int(result) < 500:
            print('{}: '.format(country) + colored('{}'.format(total_jobs_count[0].get_attribute('innerHTML')), 'red'))
        else:
            print('{}: '.format(country) + colored('{}'.format(total_jobs_count[0].get_attribute('innerHTML')), 'yellow'))
    except Exception as e:
        errors.append(country)

print('\n{}'.format(countries_json))
print('\nErrors: {}'.format(errors))
print("\n If you have errors it's cause timeout on the requests, you can run the analyzer again to try to take the results again.")