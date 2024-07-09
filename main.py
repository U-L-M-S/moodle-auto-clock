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
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
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
    moodle_login_mail = credentials['username']
    moodle_login_pswd = credentials['password']

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
    
    # Print the page source for debugging
    #print(driver.page_source)

    # Check if the button is present before waiting for it to be clickable
    button_selector = 'div.drawer-toggler.drawer-right-toggle button.btn.icon-no-margin'
    try:
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, button_selector)))
        print("Button found:", button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))).click()
    except TimeoutException:
        print("TimeoutException: Button not found or not clickable.")
        email_subject = "GFN-CLOCK-OUT ERROR Button not found"
        email_body = "Error on main.py LINE:73. Button not found or not clickable."
        mail(email_subject, email_body)
    except Exception as e:
        print(f"Exception: {e}")
        email_subject = "GFN-CLOCK-OUT ERROR"
        email_body = f"Error on main.py LINE:73. Exception: {e}"
        mail(email_subject, email_body)
    finally:
        driver.quit()


def starten():
  try:
    # Click the radio button with value "20"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @value='20']"))).click()

    # Click the "Starten" button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='btn btn-primary' and @type='submit' and @value='Starten']"))).click()
  except Exception as e:
    print(e)
    email_subject = "GFN-CLOCK-OUT ERROR starten not found"
    email_body = f"Error on main.py LINE: 94. \n 'Starten' radio button OR 'Starten' button not found.\nException: {e}"
    mail(email_subject, email_body)
  finally:
    driver.quit()

def beenden():
    try:
        # Click the sidebar toggle button to ensure it's open
        try:
            sidebar_toggle_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".drawer-toggler > .btn")))
            sidebar_toggle_button.click()
            print("Sidebar toggle button clicked to open sidebar")
        except TimeoutException:
            # Handle if sidebar toggle button is not found (assuming it's already open)
            print("Sidebar toggle button not found, assuming sidebar is already open")

        # Wait for the "Beenden" button to be present and clickable
        button_selector = ".btn-primary:nth-child(1)"  # Adjust this selector based on your actual HTML structure
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
        print("Button found:", button)

        # Click the "Beenden" button
        button.click()
        print("Button clicked")

    except TimeoutException:
        print("TimeoutException: Button not found or not clickable.")
        email_subject = "GFN-CLOCK-OUT ERROR 'Beenden' button not found"
        email_body = "Error on main.py LINE: 110. 'Beenden' button not found or not clickable."
        mail(email_subject, email_body)
    except Exception as e:
        print(f"Exception: {e}")
        email_subject = "GFN-CLOCK-OUT ERROR"
        email_body = f"Error on main.py LINE: 110. Exception: {e}"
        mail(email_subject, email_body)
    finally:
        # Quit the driver at the end of the function
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