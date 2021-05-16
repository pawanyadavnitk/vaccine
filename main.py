#Import Libraries
import os
import requests
import json
import time
# import smtplib

#Define Constants
PINCODE = "123021" #Example 600040
# MY_EMAIL = "<ENTER YOUR EMAIL ID>" #From this mail id, the alerts will be sent
# MY_PASSWORD = "<ENTER YOUR PASSWORD>" #Enter the email id's password
SLEEP_TIME = 10 #Time to wait before next request (in seconds)

#Derive the date and url
#url source is Cowin API - https://apisetu.gov.in/public/api/cowin
today = time.strftime("%d-%m-%Y")
url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"

#Write a loop which checks for every SLEEP_TIME seconds
num_check = 0
while True:
    #Start a session
    with requests.session() as session:
        num_check += 1
        print(f"Check {num_check}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = session.get(url, headers=headers)

        #Receive the response
        response = response.json()
        if not response['centers']:
            time.sleep(SLEEP_TIME)
            continue
        for center in response['centers']:
            for session in center['sessions']:

                #For Age not equal to 45 and capacity is above zero
                if (session['min_age_limit'] != 45) and (session['available_capacity'] > 0):
                    # message_string=f"Subject: {today}'s Alert'!! \n\n Available - {session['available_capacity']} in {center['name']} on {session['date']} for the age {session['min_age_limit']}"

                    # #Configure GMAIL settings
                    # with smtplib.SMTP("smtp.gmail.com") as connection:
                    #     connection.starttls()
                    #     connection.login(MY_EMAIL, MY_PASSWORD)
                    #     connection.sendmail(
                    #         from_addr=MY_EMAIL,
                    #         to_addrs=["<ENTER THE MAIL ID TO WHICH THE ALERTS HAS TO BE SENT>"], #for multiple receipients, add another email id after a comma in the list
                    #         msg=message_string
                    #     )

                    # install speech-dispather before using this -> sudo apt install speech-dispatcher
                    print(f"Vaccine is available at center: {center}")
                    os.system('spd-say "Vaccine is available. Vaccine is available. Vaccine is available."')
        time.sleep(SLEEP_TIME)