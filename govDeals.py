from selenium.webdriver.common.by import By
from datetime import date
from selenium import webdriver
import time
import config
import smtplib
import os
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


################################
################################
# Combines all of the states to the url.
def format_url() -> str:

    base_url = 'https://www.govdeals.com/closing-today/filters?stateName='

    # Formats the states names to concatenate to the url.
    for state in config.states:

        # Replaces the spaces.
        state = state.replace(' ', '%20')

        # Adds the separator for the next state.
        base_url = f"{base_url}{state}%5E"

    # Removes %5E from the last state.'
    base_url = base_url[:-3]

    # Ads the tail end of the url.
    # Sets 120 items per page.
    return f"{base_url}&pn=1&ps=120"



################################
################################
# Formats URL and scrapes the site.
# Returns all of the products as 1 full string.
def scrape_site() -> str:

    final_str = ''

    # Combines all of the states to the url.
    url = format_url()

    # Used to download current chrome driver.
    s = Service(ChromeDriverManager().install())
    
    # Creates undetected chrome driver with options.
    # Sets the process to run in the background.
    browser = uc.Chrome(use_subprocess = True,driver_executable_path = s.path)

    # Requests information from the URL.
    browser.get(url)

    # Waits for elements to load.
    time.sleep(5)

    # Get all of the product card divs.
    cards = browser.find_elements(By.XPATH, "//div[@class='card card-shadow card-products']/a")

    # Get all of the product URLS.
    item_urls = [elem.get_attribute('href') for elem in cards]

    # Get all of the product names.
    item_titles = [elem.get_attribute('title') for elem in cards]

    # Combines the product name with the url into the final string.
    for i in range(len(item_urls)):
        final_str += f"{item_titles[i]}\n{item_urls[i]}\n\n"

    # Closes webdriver.
    browser.close()
    browser.quit()

    return final_str



################################
################################
# Sends auctions via email.
# Takes in an email address and signal as strings.
def email_products(receiver: str, subject: str, email_body: str,):

    # Algo credit - https://www.google.com/search?sxsrf=ALiCzsbABYoj5xPdbPvwfr1p_R6HrBONZw:1657166767037&q=receiver&spell=1&sa=X&ved=2ahUKEwjC6-2j8-X4AhWAjIkEHY2lA8YQBSgAegQIARA0&biw=1422&bih=765&dpr=1.8

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(config.gmail_username, config.gmail_pw)

    # Message formatting.
    msg = email_body
    from_ = config.gmail_username
    to_ = receiver
    subject = subject

    # Formatted message.
    fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'

    # Sends message.
    s.sendmail(from_, to_, fmt.format(to_, from_, subject, msg).encode('utf-8'))

    # Closes SMTP session.
    s.quit()

    return



################################
################################
### MAIN
################################
################################

# Gets the full email body to send.
# Has all of the products expiring today.
email_body = scrape_site()

# Get's today's date.
today = date.today()

# Sets email subject with today's date.
subject = f"Gov Deals {today}"

# Sends the email to everyone in the email list.
# This list is in the config.py file.
for email in config.emails:
    email_products(email, subject, email_body)