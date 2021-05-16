#Import Libraries
import os
import requests
import json
import time

#Define Constants
PINCODE = "123021" #Example 600040
SLEEP_TIME = 2 #Time to wait before next request (in seconds)

#Derive the date and url
#url source is Cowin API - https://apisetu.gov.in/public/api/cowin
today = time.strftime("%d-%m-%Y")
url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"

#check for every SLEEP_TIME seconds
num_check = 0
while True:
    num_check += 1
    print(f"Check {num_check}")

    #Start a session
    with requests.session() as session:

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = session.get(url, headers=headers)

        #Receive the response
        response = response.json()

        if not response['centers']:
            time.sleep(SLEEP_TIME)
            continue

        for center in response['centers']:
            for session in center['sessions']:

                # following check can be modified
                if (session['min_age_limit'] != 45) and (session['available_capacity_dose1'] > 0):
                    print(f"Vaccine is available at center: {center}")
                    os.system('spd-say "Vaccine is available. Vaccine is available"')

        time.sleep(SLEEP_TIME)