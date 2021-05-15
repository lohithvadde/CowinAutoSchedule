import time

from login import *
from datetime import datetime


def get_districts(state_id):
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
    get_captcha()
    os.system(f'say -v "Victoria" "Enter Captcha"')
    book["captcha"] = input("Enter Captcha:")
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


def book_appointment_by_district(age: int, dose: int):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    try:
        # out = session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DISTRICT_ID}&date={DATE}")
        out = session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={DISTRICT_ID}&date={DATE}")
        if out.status_code == 200:
            for j in out.json()['centers']:
                for sessions in j['sessions']:
                    # print(f"\ncenter name: {j['name']} capacity: {sessions['available_capacity']} slots: {sessions['slots']}")
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
            os.system(f'say -v "Victoria" "Session expired"')
            print(f"status code: {out.status_code}")
            print(f"response: {out.text}")
            out = get_authenticated_session()
            if out:
                book_appointment_by_district(AGE, DOSE)
            else:
                os.system(f'say -v "Victoria" "Failed to login"')
                print("Failed to login")
                return False
        time.sleep(6)
        book_appointment_by_district(AGE, DOSE)
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        print(type(e), '::', e)
        time.sleep(6)
        out = get_authenticated_session()
        if out:
            book_appointment_by_district(AGE, DOSE)
        else:
            os.system(f'say -v "Victoria" "Failed to login"')
            print("Failed to login")
            return False


def book_appointment_by_pincodes(age: int, dose: int):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    try:
        for i in PINCODES:
            out = session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode={i}&date={DATE}")
            if out.status_code == 200:
                for j in out.json()['centers']:
                    for sessions in j['sessions']:
                        # print(f"\ncenter name: {j['name']} capacity: {sessions['available_capacity']} slots: {sessions['slots']}")
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
                os.system(f'say -v "Victoria" "Session expired"')
                print(f"status code: {out.status_code}")
                print(f"response: {out.text}")
                out = get_authenticated_session()
                if out:
                    book_appointment_by_pincodes(AGE, DOSE)
                else:
                    os.system(f'say -v "Victoria" "Failed to login"')
                    print("Failed to login")
                    return False
        time.sleep(6)
        book_appointment_by_pincodes(AGE, DOSE)
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        print(type(e), '::', e)
        time.sleep(6)
        out = get_authenticated_session()
        if out:
            book_appointment_by_pincodes(AGE, DOSE)
        else:
            os.system(f'say -v "Victoria" "Failed to login"')
            print("Failed to login")
            return False


if __name__ == '__main__':
    if GET_DISTRICT_IDS:
        get_districts({GET_DISTRICT_IDS})
    else:
        out = get_authenticated_session()
        if out:
            if DISTRICT_ID:
                book_appointment_by_district(AGE, DOSE)
            elif PINCODES:
                book_appointment_by_pincodes(AGE, DOSE)
            else:
                os.system(f'say -v "Victoria" "Please enter district id or pin codes"')
                print("Please enter district id or pin codes")
                exit(1)
        else:
            os.system(f'say -v "Victoria" "Failed to login"')
            print("Failed to login")
