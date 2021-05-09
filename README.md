# CoWin-Auto-Schedule
## A Python 3 Script to Schedule CoWin Vaccination Appointment. This script supports Captcha.  

### Please add/change REGISTERED_MOBILE_NUMBER, Beneficiaries_Ids (Get this by logging into Cowin) and District ids (Use Cowin public APIs) as per your choice 

After successfull login, Script will iterate over given District and will try to book appointment directly where slots are available to book. It is important to specify only desired District. Script won't ask you to choose center/slots/vaccine or any of the parameter.

Once script finds the available slot, it will automatically download captcha in ```svg.html``` file. Script will ask you to enter the captcha and press ```enter```. The ```svg.html``` file will be present under current working directory. Please note capcha is **case sensitive**
    
    
Note: 

*This script will only help you to book the slot using given District if slots are available. If slots are already full script will keep on running until it finds slots and book*
*This Script will book appointment for next day by default. If you wish to change this behaviour you can edit DATE variable in config.py*
*Script is tested for both 18-44 and 45+ group for first dose only*
*You can also run this based on pincodes. Check bookkeeping folder for the api call. Makesure to not give more than 5 pincodes because of rate limitation*
*If you want this for the second dose, change the dose value to 2*
*Keep on feeding the Mobile OTP's whenever session expires. Don't worry ! This is easy, because you ll get an alert by system sounds"
