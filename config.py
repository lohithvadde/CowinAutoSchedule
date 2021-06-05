from datetime import timedelta, datetime
DATE = (datetime.today() + timedelta(1)).strftime("%d-%m-%Y")  # timedelta(1) means any dates from tomorrow.

LIMIT = 3  # otp retry limit
SLEEP_TIME = 3.5  # Change this to 5 or more when doing by pin code
CAPTCHA_MODE = 'NOCAPTCHA'  # AUTO or MANUAL or PREMIUM or EXTRAORDINARY or NOCAPTCHA

DISTRICT_ID = 395  # Check Book keeping folder for district ids. If it's not there, enter state id in the GET_DISTRICT_IDS and run.
PINCODES = [400002]  # Put DISTRICT_ID = 0 when you enter pin codes. Don't use more than 4 pin codes

REGISTERED_MOBILE_NUMBER = 6363640877  # 10 digit mobile number in int
BENEFICIARY_IDS = {
    '18':["93433417992070","12709797522520"],
    '45':[""]
}  # beneficiary ids in str format and comma separated ids
AGE = 18
DOSE = 1
VACCINE = 'COVAXIN'  # 'ANY' or 'COVISHIELD' or 'COVAXIN' or 'SPUTNIK'

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