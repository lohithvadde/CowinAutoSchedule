from datetime import timedelta, datetime
DATE = (datetime.today() + timedelta(1)).strftime("%d-%m-%Y")

LIMIT = 3  # otp retry limit
SLEEP_TIME = 3.5
CAPTCHA_MODE = 'AUTO'  # AUTO or MANUAL

DISTRICT_ID = 395  # Check Book keeping folder for district ids. If it's not there, enter state id in the GET_DISTRICT_IDS and run.
PINCODES = [560001,560002,560003,560004]  # Put DISTRICT_ID = 0 when you enter pin codes

REGISTERED_MOBILE_NUMBER = 9372810220  # 10 digit mobile number in int
BENEFICIARY_IDS = {
    '18':["62867477281530"],
    '45':[""]
}  # beneficiary ids in str format and comma separated ids
AGE = 18
DOSE = 1
VACCINE = 'ANY'  # 'ANY' or 'COVISHIELD' or 'COVAXIN' or 'SPUTNIK'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Origin': 'https://selfregistration.cowin.gov.in',
    'Connection': 'keep-alive',
    'Referer': 'https://selfregistration.cowin.gov.in/',
    'TE': 'Trailers',
}

GET_DISTRICT_IDS = 0