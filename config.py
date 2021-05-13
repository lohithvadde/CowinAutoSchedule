from datetime import timedelta, datetime
DATE = (datetime.today() + timedelta(1)).strftime("%d-%m-%Y")
LIMIT = 3 #otp retry limit

PINCODES = [560001,560002,560003,560004,560005,560006,560008,560010,560011,560013,560014,560016,560018,
            560019,560020,560021,560022,560023,560026,560027,560028,560029,560030,560032,560033,560035,
            560036,560037,560038,560039,560040,560045,560047,560048,560049,560050,560051,560054,560056,
            560057,560058,560060,560063,560064,560066,560067,560068,560069,560070,560071,560073,560074,
            560076,560077,560078,560079,560083,560084,560086,560087,560088,560089,560090,560091,560092,
            560093,560096,560097,560098,560099,560105,560106,560112,560116,562106,562107,562123,562125,
            562130,562149,562157,562162] #list of pincodes by your preference.

DISTRICT_ID = 294 #Check Book keeping folder

REGISTERED_MOBILE_NUMBER = 6363640877 # 10 digit mobile number in int

Beneficiaries_Ids = {
    '18':["47494580941600","69372972731330","80273475067100","48772031718880"],
    '45':[""]
} #beneficiary ids in str format

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