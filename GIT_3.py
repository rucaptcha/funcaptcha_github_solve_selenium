import gzip
import os
import re
import time
import seleniumwire.undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha #pip3 install 2captcha-python


import chromedriver_autoinstaller_fix

def intercept_request(request):
    if "https://github-api.arkoselabs.com/fc/gt2/public_key/747B83EC-2CA3-43AD-A7DF-701F286FBABA" in request.url:
        request.abort()
        print("BLOCKED THIS REQUEST ------", request.url)

def intercept_response(request, response):
    if "https://octocaptcha.com/?origin_page=github_signup_redesign&responsive=true" in request.url:
        print(request.url)
        data_captcha = str(gzip.decompress(response.body))
        pattern = r'data-data-exchange-payload="([^"]+)'
        global data_blob
        data_blob = re.search(pattern, data_captcha).group(1)

my_key = os.environ["APIKEY"]
solver = TwoCaptcha(my_key)
data_blob = ""
proxy5 = "xxxxx:xxxxxx@xxx.xx.xxx.xx:8000"#Polska
chromedriver_autoinstaller_fix.install()
options = {'proxy': {'https': 'https://' + proxy5}}
chrome_options = uc.ChromeOptions()

driver = webdriver.Chrome(seleniumwire_options=options)
driver.request_interceptor = intercept_request
driver.response_interceptor = intercept_response
url = "https://github.com/signup"
driver.get(url)
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, '#email').send_keys('alter_shmalter2000@gmail.com')
time.sleep(4)
driver.find_element(By.CSS_SELECTOR, "#email-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button").click()
time.sleep(4)
driver.find_element(By.CSS_SELECTOR, '#password').send_keys('password2000AA##22')
time.sleep(4)
driver.find_element(By.CSS_SELECTOR, "#password-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button").click()
time.sleep(4)
driver.find_element(By.CSS_SELECTOR, "#login").send_keys("AlexStorm2022")
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "#username-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button").click()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "#opt_in").click()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "#opt-in-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button").click()
time.sleep(10)
print("Data_blob received: ", data_blob)

try:
    print("Captcha solve...")
    result = solver.funcaptcha(
        sitekey="747B83EC-2CA3-43AD-A7DF-701F286FBABA",
        url=url,
        surl="https://github-api.arkoselabs.com",
        **{'data[blob]': data_blob},
        proxy={'type': 'HTTP', 'uri': proxy5}
    )
except Exception as e:
    print(e)
    driver.quit()
else:
    print("Captcha solved!")
    print(result)
solution = result["code"]
driver.execute_script("document.getElementsByName('octocaptcha-token')[0].value = arguments[0];", solution)
print("token inserted!!")
driver.find_element(By.CSS_SELECTOR, "#captcha-and-submit-container > div:nth-child(6) > button").click()
time.sleep(20)


driver.quit()