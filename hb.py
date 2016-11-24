#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import getpass
import json
import requests
from progress.bar import Bar

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

reload(sys)
sys.setdefaultencoding('utf-8')

message = ''
M = 'male'
F = 'female'
NOT_SURE = 'gender uncertainty'
bar = Bar('Processing', max=5)
NAME = 'NAME'

driver = webdriver.PhantomJS()
# For testing only
# driver = webdriver.Chrome('./chromedriver')

if len(sys.argv) > 2 and sys.argv[1] == '-m':
    message = sys.argv[2]
# Auth
EMAIL = raw_input('email: ')
PASSWD = getpass.getpass('password: ')

def check_gender(name):
    res = json.loads(requests.get("https://api.genderize.io/", {'name': name}).text)
    prob = res['probability']
    if prob < 0.90:
        return NOT_SURE
    return res['gender']

"""
    @TO-DO: "Put this in another script"
"""
def format_message(user_name):
    first_name = user_name.split(' ')[0]
    if message != '':
        if NAME in message:
            new_message = message.replace(NAME, first_name)
            return new_message
        return message
    else:
        gender = check_gender(first_name)
        if gender == M:
            return "Parabéns "+first_name+" :D ! Abraço"
        elif gender == F:
            return "Parabéns "+first_name+" ;) ! Beijinhos"
        else:
            return "Parabéns "+first_name+" :) Felicidades"

"""
    @TO-DO: "Filter 'See Friendship' in report"
    A concise report about people who have celebrate their birthday in
    a recent past, or the ones that are to come in a near future.
"""
def print_birthdays_full_report():
    login_facebook()
    go_to_birthdays_page()
    birthdays = driver.find_element_by_xpath("//div[@id='events_birthday_view'][1]")
    print birthdays.text

"""
    Enter facebook with the provided credentials
"""
def login_facebook():
    driver.get('https://www.facebook.com/')
    driver.find_element_by_id('email').send_keys(EMAIL)
    driver.find_element_by_id('pass').send_keys(PASSWD)
    driver.find_element_by_id('loginbutton').click()

"""
    Go to facebook's birthdays page
"""
def go_to_birthdays_page():
    driver.get('https://www.facebook.com/events/birthdays')

"""
    Wish a happy birthday to people who celebrate
    their special time today (being 'today' the day you run the script)
"""
def wish_a_happy_birthday():
    bar.next()
    login_facebook()
    bar.next()
    time.sleep(2)
    bar.next()
    go_to_birthdays_page()
    bar.next()

    list_of_bdays = driver.find_elements_by_xpath("//ul[@class='_3ng0']//li")
    if list_of_bdays is not None:
        try:
            for li in list_of_bdays:
                # Please get this by xpath expression instead of split
                fields = li.text.split('\n')
                try:
                    text_area = li.find_element_by_xpath('.//textarea')
                    if text_area is not None:
                        text_area.send_keys(format_message(fields[0]))
                        text_area.send_keys(Keys.ENTER)
                except:
                    bar.next()
                    continue
        except:
            bar.next()

"""
    @TO-DO: "List recent birthdays"
    This is a proof of concept for the iterative process on the list items
    of facebook birthday events.
    This is applied to the section "Recent Birthdays", but the final goal
    is to apply the same procedure to the "Today's Birthdays" section.
"""
def list_recent_birthdays():
    login_facebook()
    go_to_birthdays_page()
    friends = driver.find_elements_by_xpath("//li[@class='_43q7']//img")
    print "Some Brithdays"
    for f in friends:
        print f.get_attribute('alt')

# Call main task
wish_a_happy_birthday()
