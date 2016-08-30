import sys
import getpass
import json
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

message = ""
M = 'male'
F = 'feminine'
NOT_SURE = 'gender uncertainty'

driver = webdriver.PhantomJS()

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
    gender = check_gender(first_name)
    if gender == M:
        return "Parabens "+first_name+" :D ! Abraco"
    elif gender == F:
        return "Parabens "+first_name+" ;D ! Beijinhos"
    else:
        return "Parabens "+first_name+" :) Felicidades"

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
    login_facebook()
    go_to_birthdays_page()
    # For each birtday boy or girl leave a (before u have to build it)
    # message and click the 'Publish' button
    #p = driver.find_element_by_class_name('fwn').find_ ...
    div = driver.find_element_by_id('events_birthday_view')
    if div is not None:
        try:
            users_names = driver.find_element_by_class_name('_3ng2')
            print users_names
            # @TO-DO[1]: "Missing for loop for each users_name in users_names"
            #text_areas = driver.find_element_by_xpath("//div[@class='innerWrap'][1]//textarea[1]")
            #text_areas.send_keys(format_message(users_names.text))
            #text_areas.send_keys(Keys.RETURN)
        except:
            print "Maybe today is nobody's birthday :("

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
# wish_a_happy_birthday()

# Call future birthday's provisionary
# print_birthdays_full_report()
list_recent_birthdays()
