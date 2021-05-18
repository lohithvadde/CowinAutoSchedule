from datetime import timedelta, datetime
DATE = (datetime.today() + timedelta(1)).strftime("%d-%m-%Y")

LIMIT = 3 #otp retry limit
SLEEP_TIME = 3.5

DISTRICT_ID = 363 #Check Book keeping folder
PINCODES = [560001,560002,560003,560004] #list of pincodes by your preference.

REGISTERED_MOBILE_NUMBER = 9711987543 # 10 digit mobile number in int

BENEFICIARY_IDS = {
    '18':["97207920685230","60707677673280","23764339707240"],
    '45':[""]
} #beneficiary ids in str format

AGE = 18
DOSE = 1

VACCINE = 'COVISHIELD' #'COVISHIELD' or 'COVAXIN' in case of dose 2. for dose 1, it does not matter what is the vaccine type given here script will book whichever is available

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