from datetime import timedelta, datetime
DATE = (datetime.today() + timedelta(1)).strftime("%d-%m-%Y")
LIMIT = 3 #otp retry limit

PINCODES = [560001,560002,560003,560004] #list of pincodes by your preference.

DISTRICT_ID = 363 #Check Book keeping folder

REGISTERED_MOBILE_NUMBER = 9848022338 # 10 digit mobile number in int

Beneficiaries_Ids = {
    '18':["47494580941600","69372972731330","80273475067100","48772031718880"],
    '45':[""]
} #beneficiary ids in str format

AGE = 18

DOSE = 1

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