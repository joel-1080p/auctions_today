# auctions_today

## Purpose
auctions_today gets all of the auctions ending today from govDeals.com (more comming soon).
You can set your current state and surrounding states as a paramiter to pull from.
When the app finishes, you will get an email with all of the auctions ending today.

![IMG_1743](https://github.com/joel-1080p/auctions_today/assets/156847809/9d2080fd-95f8-4b50-9c98-e2a846b92216)

## How To Use
- Edit `config.py` with the states you want to get auctions from.
- In `config.py` edit `emails` list to edit the emails you want to send the emails to.
- In `config.py` change `gmail_username` and `gmail_pw` to change the email it's going to be sending from.
- Run `govDeals.py` to get all of the acutions ending that day.

NOTE : Set up app passwords for this to work with Gmail.

## How I Use It
I have this script runnig daily at 5 AM using Windows Task Scheduler.

## Libraries
- Latest Python
- Selinium Webdriver
- smtplib
- datetime
- undetected_chromedriver

## P.S.

Please drop me a note with any feedback you have.

**Joel**
