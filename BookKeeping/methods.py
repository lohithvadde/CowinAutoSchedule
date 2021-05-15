import time

from login import *

def get_beneficiaries():
    beneficiaries = session.get('https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries')
    if beneficiaries.status_code == 200:
        print("Successfully Fetch Beneficiaries")
        print(beneficiaries.json())
    else:
        print(f"Beneficiaries Status_code: {beneficiaries.status_code}\n{beneficiaries.text}")

def book_slot(book):
    print(f"Trying to book: {book}")
    get_captcha()
    book["captcha"] = input("Enter Captcha:")
    os.system(f'say -v "Victoria" "Enter Captcha"')
    book = json.dumps(book)
    resp = session.post("https://cdn-api.co-vin.in/api/v2/appointment/schedule", data=book)
    if resp.status_code == 200:
        print("Scheduled Successfully.")
        print(f"response: {resp.json()}")
        return True
    else:
        print(f"booking error. {resp.status_code}\n{resp.text}")
        return False

def get_captcha():
    out = session.post("https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha")
    if out.status_code == 200:
        captcha = out.json()['captcha']                                                                                                                                                                     
        with open("svg.html", "w") as f: 
            f.write(captcha)
        print("captcha downloaded successfully")
      

def book_appointment_by_pincodes(age=18, dose=1):
    for i in PINCODES:
        out = session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={i}&date={DATE}")
        if out.status_code == 200:
            for j in out.json()['centers']:
                for sessions in j['sessions']:
                    print(f"\ncenter name: {j['name']} capacity: {sessions['available_capacity']} slots: {sessions['slots']}")
                    if sessions['available_capacity'] > 0 and sessions['min_age_limit'] == age:
                        book = {
                            "center_id": j['center_id'],
                            "session_id": sessions['session_id'],
                            "beneficiaries": BENEFICIARY_IDS[f"{age}"],
                            "slot": sessions['slots'][0],
                            "dose": dose
                        }
                        stop = book_slot(book)
                        if stop:
                            print("booking successfull")
                            return True
        else:
            print(f"status code: {out.status_code}")
            print(f"response: {out.text}")

def book_appointment_by_district(age=18, dose=1):
    try:
        out = session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DISTRICT_ID}&date={DATE}")
        if out.status_code == 200:
            for j in out.json()['centers']:
                for sessions in j['sessions']:
                    print(f"\ncenter name: {j['name']} capacity: {sessions['available_capacity']} slots: {sessions['slots']}")
                    if sessions['available_capacity'] > 0 and sessions['min_age_limit'] == age:
                        print(f"\ncenter name: {j['name']} capacity: {sessions['available_capacity']} slots: {sessions['slots']}")
                        book = {
                            "center_id": j['center_id'],
                            "session_id": sessions['session_id'],
                            "beneficiaries": BENEFICIARY_IDS[f"{age}"],
                            "slot": sessions['slots'][0],
                            "dose": dose
                        }
                        stop = book_slot(book)
                        if stop:
                            os.system(f'say -v "Victoria" "Booking Successful"')
                            print("Booking Successful")
                            return True
        else:
            print(f"status code: {out.status_code}")
            print(f"response: {out.text}")
        time.sleep(20)
        book_appointment_by_district(age=18)
    except ConnectionResetError:
        os.system(f'say -v "Victoria" "Connection Reset Error"')
        print("Connection Reset Error")


    
def captchaAlert(msg = "Enter Captcha", voice = "Victoria"):
    os.system(f'say -v {voice} {msg}')

def otpAlert(msg = "Enter OTP", voice = "Victoria"):
    os.system(f'say -v {voice} {msg}')

if __name__ == '__main__':
    out = get_authenticated_session()
    if out != False:
        book_appointment_by_district(age=18)
        # get_beneficiaries()

        # Book appointment by pincodes doesn't run in an infinite loop. This is because of rate limitation
        # book_appointment_by_pincodes(age=18)
        # book_appointment_by_pincodes(age=45)
    else:
        print("Failed to login")
