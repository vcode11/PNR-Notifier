from selenium import webdriver
import smtplib
import getpass
import time

def check_pnr_status(pnr):
    browser = webdriver.Firefox()
    browser.get('https://trainspnrstatus.com')
    pnrelem = browser.find_element_by_id('fullname')
    pnrelem.send_keys(str(pnr))
    time.sleep(2)
    pnrelem.submit()
    time.sleep(5)
    td = browser.find_elements_by_tag_name('td')
    current_status = td[22].text + ' and is ' + td[24].text
    browser.quit()
    if 'chart' in current_status.lower():
        return current_status
    else:
        return 'IP Blocking'

def send_pnr_status_mail(email, password, pnr):
    current_status = check_pnr_status(pnr)
    smtp_server = 'smtp.gmail.com'
    port = 587
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        server.sendmail(email, email, f'Subject:PNR Status\n\n Your current status for PNR NO. {pnr} is {current_status}')
        server.quit()
        print(f'A email has been sent to {email}')
    except Exception as e:
        print(e)
        
email = input('Enter the email to recieve pnr status.')
password = getpass.getpass()
pnr = input('Enter pnr no.')
time_to_wait = 3600 # 3600 seconds in an hour

while True:
    send_pnr_status_mail(email, password, pnr)
    time.sleep(one_hour)

