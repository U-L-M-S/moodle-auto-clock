import requests
import smtplib
import json
import os
from bs4 import BeautifulSoup

LOGIN_URL = "https://lernplattform.gfn.de/login/index.php"
START_URL = "https://lernplattform.gfn.de/?starten=1"
STOP_URL = "https://lernplattform.gfn.de/?stoppen=1"

def mail(subject, body):
    """Send error/success emails"""
    with open('credentials.local.json') as f:
        creds = json.load(f)
    bot_mail = creds['bot_mail']
    bot_pswd = creds['bot_pswd']
    user_mail = creds['user_mail']

    headers = "\r\n".join([
        f"From: {bot_mail}",
        f"To: {user_mail}",
        f"Subject: {subject}",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8"
    ])

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(bot_mail, bot_pswd)
    session.sendmail(bot_mail, user_mail, headers + "\r\n\r\n" + body)
    session.quit()


def login():
    """Login to Moodle using requests.Session() and return the session"""
    with open('credentials.local.json') as f:
        creds = json.load(f)

    s = requests.Session()

    # Step 1 – get login token
    resp = s.get(LOGIN_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    token = soup.find('input', {'name': 'logintoken'})
    logintoken = token['value'] if token else ""

    # Step 2 – send login POST
    payload = {
        'username': creds['username'],
        'password': creds['password'],
        'logintoken': logintoken
    }
    resp = s.post(LOGIN_URL, data=payload)

    if resp.status_code != 200 or "login" in resp.url:
        mail("GFN-CLOCK LOGIN FAILED", "Login to Moodle failed — check credentials.")
        raise Exception("Login failed")

    print("Logged in successfully.")
    return s


def starten(session):
    """Send the start request"""
    payload = {'homeo': '2'}  
    resp = session.post(START_URL, data=payload)
    print(f"Starten → {resp.status_code}")
    if resp.status_code == 200:
        mail("GFN-CLOCK STARTED", "Successfully clocked IN on Moodle.")
    else:
        mail("GFN-CLOCK START ERROR", f"Response: {resp.status_code}")


def beenden(session):
    """Send the stop request"""
    resp = session.post(STOP_URL)
    print(f"Beenden → {resp.status_code}")
    if resp.status_code == 200:
        mail("GFN-CLOCK STOPPED", "Successfully clocked OUT on Moodle.")
    else:
        mail("GFN-CLOCK STOP ERROR", f"Response: {resp.status_code}")


def main(action):
    try:
        session = login()
        if action == "starten":
            starten(session)
        elif action == "beenden":
            beenden(session)
        else:
            mail("GFN-CLOCK UNKNOWN ACTION", f"Unknown ACTION: {action}")
    except Exception as e:
        mail("GFN-CLOCK ERROR", str(e))


if __name__ == "__main__":
    action = os.environ.get("ACTION")
    if not action:
        mail("GFN-CLOCK MISSING ACTION",
             "Please pass ACTION=starten or ACTION=beenden.")
    else:
        main(action)

