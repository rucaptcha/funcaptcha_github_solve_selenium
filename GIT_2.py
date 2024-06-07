import gzip
import os
import re
from seleniumbase import Driver
from twocaptcha import TwoCaptcha #pip3 install 2captcha-python

data_blob = ""

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
        print("Data_blob received: ", data_blob)

conf = {
    'apiKey': os.environ["APIKEY"],
    'defaultTimeout': 600
}

solver = TwoCaptcha(**conf)

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
driver = Driver(wire=True, proxy=False, headless=False, agent=agent, devtools=True)
try:
    driver.request_interceptor = intercept_request
    driver.response_interceptor = intercept_response
    url = "https://github.com/signup"
    driver.get(url)
    driver.type('#email', 'alter_shmalter2000@gmail.com')
    driver.sleep(4)
    driver.click("#email-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button")
    driver.sleep(4)
    driver.type('#password', 'password2000AA##22')
    driver.sleep(4)
    driver.click("#password-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button")
    driver.sleep(4)
    driver.type("#login", "AlexStorm2022")
    driver.sleep(5)
    driver.click("#username-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button")
    driver.sleep(3)
    driver.click("#opt_in")
    driver.sleep(3)
    driver.click("#opt-in-container > div.d-flex.flex-items-center.flex-column.flex-sm-row > button")
    driver.sleep(10)
    curr_url = driver.current_url
    
    # driver.sleep(500)

    try:
        print("Captcha solve...")
        result = solver.funcaptcha(
            sitekey="747B83EC-2CA3-43AD-A7DF-701F286FBABA",
            url=curr_url,
            surl="https://github-api.arkoselabs.com",
            userAgent=agent,
            **{'data[blob]': data_blob}
            # proxy={'type': 'HTTP', 'uri': proxy1}
        )
    except Exception as e:
        print(e)
        driver.quit()
    else:
        print("Captcha solved!")
        print(result)
    solution = result["code"]
    driver.execute_script("document.getElementsByName('octocaptcha-token')[0].value = arguments[0];", solution)
    driver.switch_to_frame("iframe.js-octocaptcha-frame")
    driver.execute_script("parent.postMessage({ event: 'captcha-complete', sessionToken: arguments[0] }, 'https://github.com')", solution)
    print("token inserted!!")
    # driver.click("#captcha-and-submit-container > div:nth-child(6) > button")
    driver.sleep(50)
except Exception as e:
    print(e)
finally:
    driver.quit()
