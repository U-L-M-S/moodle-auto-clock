from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
import json
import os

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options) 
login_url = 'https://lernplattform.gfn.de/login/index.php'
driver.get(login_url)

def mail(email_subject, email_body)->None:
    with open('credentials.json') as f:
        credentials = json.load(f)
    bot_mail=credentials['bot_mail']
    bot_pswd=credentials['bot_pswd']
    user_mail=credentials['user_mail']

    # standard email Variables
    SMTP_SERVER = 'smtp.gmail.com' # Email Server (don't change!)
    SMTP_PORT = 587 # Server Port (don't change!)
        
    # Create Headers
    email_headers = "\r\n".join(['From: ' + bot_mail,
                            'Subject: ' + email_subject,
                            'To: ' + user_mail,
                            'MIME-Version: 1.0',
                            'Content-Type: text/html'])
    
    # Connect to Server
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    # Login to Server
    session.login(bot_mail, bot_pswd)

    # Send Email & Exit
    session.sendmail(bot_mail, user_mail, email_headers + "\r\n\r\n" + email_body)
    session.quit()

def login()->None:
    with open('credentials.json') as f:
        credentials = json.load(f)
    moodle_login_mail=credentials['username']
    moodle_login_pswd=credentials['password']

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(moodle_login_mail)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(moodle_login_pswd)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginbtn'))).click()

    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert accepted")
    except TimeoutException:
        print("No alert")

def get_cookies():
    """Fetch the necessary cookies after logging in"""
    cookies = driver.get_cookies()
    moodle_session = None
    moodleid1 = None
    
    for cookie in cookies:
        if cookie['name'] == 'MoodleSession':
            moodle_session = cookie['value']
        elif cookie['name'] == 'MOODLEID1_':
            moodleid1 = cookie['value']
    
    return moodle_session, moodleid1

def starten():
    # Use triple quotes without `f` to avoid interpreting `{}` as placeholders in Python.
    post_request_script = """
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/?starten=1", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("Cookie", "EU_COOKIE_LAW_CONSENT=true; MoodleSession={moodle_session}; MOODLEID1_={moodleid1}");
    xhr.setRequestHeader("Cache-Control", "max-age=0");
    xhr.setRequestHeader("Sec-Ch-Ua", '"Not?A_Brand";v="99", "Chromium";v="130"');
    xhr.setRequestHeader("Sec-Ch-Ua-Mobile", "?0");
    xhr.setRequestHeader("Sec-Ch-Ua-Platform", '"Linux"');
    xhr.setRequestHeader("Accept-Language", "de-DE,de;q=0.9");
    xhr.setRequestHeader("Origin", "https://lernplattform.gfn.de");
    xhr.setRequestHeader("Upgrade-Insecure-Requests", "1");
    xhr.setRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36");
    xhr.setRequestHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7");
    xhr.setRequestHeader("Sec-Fetch-Site", "same-origin");
    xhr.setRequestHeader("Sec-Fetch-Mode", "navigate");
    xhr.setRequestHeader("Sec-Fetch-User", "?1");
    xhr.setRequestHeader("Sec-Fetch-Dest", "document");
    xhr.setRequestHeader("Referer", "https://lernplattform.gfn.de/");
    xhr.setRequestHeader("Accept-Encoding", "gzip, deflate, br");
    xhr.setRequestHeader("Priority", "u=0, i");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log("POST request completed successfully with status:", xhr.status);
            } else {
                console.log("Error in POST request with status:", xhr.status);
            }
        }
    };

    xhr.send("homeo=2");
    """
    driver.execute_script(post_request_script)


def beenden():
    driver.get('https://lernplattform.gfn.de/?stoppen=1')
    driver.quit()

def main(action:str)->None:
    login()
    if action == "starten":
        starten()
    if action == "beenden":
        beenden()

if __name__ == "__main__":
    action=os.environ.get('ACTION')
    if action == None or action == "":
        email_subject = "GFN-CLOCK-OUT ERROR ENTRY"
        email_body = f"No action specified LINE:98. Please specify an action in the environment variables.\n ACTION is probably empty or not set."
        mail(email_subject, email_body)
    else:
        main(action)

