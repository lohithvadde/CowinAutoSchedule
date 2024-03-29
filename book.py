import _thread
import time

import captcha
from login import *
from datetime import datetime
from captcha import captcha_builder_manual, captcha_builder_auto, captcha_builder_premium, captcha_builder_extraordinary

global DATE


def get_districts(state_id: int):
    url = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}"
    url = url.replace("{", "").replace("}", "")
    out = session.get(url)
    if out.status_code == 200:
        output = out.json()
        for j in output["districts"]:
            print(j)


def get_beneficiaries():
    beneficiaries = session.get('https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries')
    if beneficiaries.status_code == 200:
        print("Successfully Fetch Beneficiaries")
        print(beneficiaries.json())
    else:
        print(f"Beneficiaries Status_code: {beneficiaries.status_code}\n{beneficiaries.text}")


def book_slot(book):
    print(f"Trying to book: {book}")
    if CAPTCHA_MODE != 'NOCAPTCHA':
        captcha_result = get_captcha()
        if captcha_result == 'None' or len(captcha_result) < 5:
            print(f"Trying captcha again")
            captcha_result = get_captcha()  # sometimes we don't get captcha in the first attempt or the captcha has just 4 letters
        book["captcha"] = captcha_result
    book = json.dumps(book)
    resp = session.post("https://cdn-api.co-vin.in/api/v2/appointment/schedule", data=book)
    if resp.status_code == 200:
        print(f"response: {resp.json()}")
        return True
    else:
        print(f"booking error. {resp.status_code}\n{resp.text}")
        return False


def get_captcha():
    if CAPTCHA_MODE == 'PREMIUM':
        return captcha.captcha_text_decoded
    else:
        out = session.post("https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha")
        if out.status_code == 200:
            if CAPTCHA_MODE == 'MANUAL':
                captcha_response = out.json()['captcha']
                with open("svg.html", "w") as f:
                    f.write(captcha_response)
                print("captcha downloaded successfully")
                os.system(f'say -v "Victoria" "Enter Captcha"')
                return captcha_builder_manual(out.json())
            elif CAPTCHA_MODE == 'AUTO':
                return captcha_builder_auto(out.json())
            elif CAPTCHA_MODE == 'EXTRAORDINARY':
                captcha_resp = captcha_builder_extraordinary(session.headers)
                if not captcha_resp:
                    print("Could not read captcha from string, found empty captcha")
                    return captcha_builder_auto(out.json())
                else:
                    return captcha_resp
        else:
            return 'None'


def find_appointment_by_district(age: int, dose: int):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    try:
        out = session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/findByDistrict?district_id={DISTRICT_ID}&date={DATE}")
        if out.status_code == 200:
            for sessions in out.json()['sessions']:
                if sessions['available_capacity'] > len(BENEFICIARY_IDS[f"{age}"]) and sessions['min_age_limit'] == age and (sessions['fee_type'] == FEE_TYPE or FEE_TYPE == 'Any'):
                    if (DOSE == 1 and sessions['available_capacity_dose1'] > len(BENEFICIARY_IDS[f"{age}"]) and (VACCINE == 'ANY' or VACCINE == sessions['vaccine'])) or \
                            (DOSE == 2 and sessions['available_capacity_dose2'] > len(BENEFICIARY_IDS[f"{age}"]) and VACCINE == sessions['vaccine']):
                        print(f"\ncenter name: {sessions['name']} capacity: {sessions['available_capacity']} slots: {sessions['slots']}")
                        book = {
                            "center_id": sessions['center_id'],
                            "session_id": sessions['session_id'],
                            "beneficiaries": BENEFICIARY_IDS[f"{age}"],
                            "slot": sessions['slots'][0],
                            "dose": dose
                        }
                        stop = book_slot(book)
                        if stop:
                            os.system(f'say -v "Victoria" "Booking Successful"')
                            print("Booking Successful")
                            now = datetime.now()
                            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                            print("date and time =", dt_string)
                            return True
        else:
            os.system(f'say -v "Victoria" "Session expired"')
            print(f"status code: {out.status_code}")
            print(f"response: {out.text}")
            time.sleep(SLEEP_TIME)
            out = get_authenticated_session()
            if out:
                find_appointment_by_district(AGE, DOSE)
            else:
                os.system(f'say -v "Victoria" "Failed to login"')
                print("Failed to login")
                return False
        time.sleep(SLEEP_TIME)
        find_appointment_by_district(AGE, DOSE)
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        print(type(e), '::', e)
        time.sleep(SLEEP_TIME)
        out = get_authenticated_session()
        if out:
            find_appointment_by_district(AGE, DOSE)
        else:
            os.system(f'say -v "Victoria" "Failed to login"')
            print("Failed to login")
            return False


def find_appointment_by_pincodes(age: int, dose: int):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    try:
        for i in PINCODES:
            out = session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/findByPin?pincode={i}&date={DATE}")
            if out.status_code == 200:
                for sessions in out.json()['sessions']:
                    if sessions['available_capacity'] > len(BENEFICIARY_IDS[f"{age}"]) and sessions['min_age_limit'] == age and (sessions['fee_type'] == FEE_TYPE or FEE_TYPE == 'Any'):
                        if (DOSE == 1 and sessions['available_capacity_dose1'] > len(BENEFICIARY_IDS[f"{age}"]) and (VACCINE == 'ANY' or VACCINE == sessions['vaccine'])) or \
                                (DOSE == 2 and sessions['available_capacity_dose2'] > len(BENEFICIARY_IDS[f"{age}"]) and VACCINE == sessions['vaccine']):
                            print(f"\ncenter name: {sessions['name']} capacity: {sessions['available_capacity']} slots: {sessions['slots']}")
                            book = {
                                "center_id": sessions['center_id'],
                                "session_id": sessions['session_id'],
                                "beneficiaries": BENEFICIARY_IDS[f"{age}"],
                                "slot": sessions['slots'][0],
                                "dose": dose
                            }
                            stop = book_slot(book)
                            if stop:
                                os.system(f'say -v "Victoria" "Booking Successful"')
                                print("Booking Successful")
                                now = datetime.now()
                                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                                print("date and time =", dt_string)
                                return True
            else:
                os.system(f'say -v "Victoria" "Session expired wait for 30 seconds"')
                print(f"status code: {out.status_code}")
                print(f"response: {out.text}")
                time.sleep(SLEEP_TIME)
                out = get_authenticated_session()
                if out:
                    find_appointment_by_pincodes(AGE, DOSE)
                else:
                    os.system(f'say -v "Victoria" "Failed to login"')
                    print("Failed to login")
                    return False
        time.sleep(SLEEP_TIME)
        find_appointment_by_pincodes(AGE, DOSE)
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        print(type(e), '::', e)
        time.sleep(SLEEP_TIME)
        out = get_authenticated_session()
        if out:
            find_appointment_by_pincodes(AGE, DOSE)
        else:
            os.system(f'say -v "Victoria" "Failed to login"')
            print("Failed to login")
            return False


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    if GET_DISTRICT_IDS:
        get_districts(GET_DISTRICT_IDS)
    else:
        out = get_authenticated_session()
        if out:
            if CAPTCHA_MODE == 'PREMIUM':
                try:
                    _thread.start_new_thread(captcha_builder_premium, (100, session.headers, 1))
                except:
                    print("Error: unable to start thread")
            global DATE
            delta = input("Enter delta 0 for today or 1 for tmrw or 2 for day after.... Default is 1 if you don't enter anything ====>")
            if delta == '0' or delta == '2':
                DATE = (datetime.today() + timedelta(int(delta))).strftime("%d-%m-%Y")
            else:
                DATE = (datetime.today() + timedelta(1)).strftime("%d-%m-%Y")

            if DISTRICT_ID:
                find_appointment_by_district(AGE, DOSE)
            elif PINCODES:
                find_appointment_by_pincodes(AGE, DOSE)
            else:
                os.system(f'say -v "Victoria" "Please enter district id or pin codes"')
                print("Please enter district id or pin codes")
                exit(1)
        else:
            os.system(f'say -v "Victoria" "Failed to login"')
            print("Failed to login")