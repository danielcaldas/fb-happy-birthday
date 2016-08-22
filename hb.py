import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

"""
    @TO-DO: "Ask for password in runtime, instead of supply it via terminal"
"""
if len(sys.argv) != 3:
    print "You provided a wrong number of arguments."
    sys.exit()

EMAIL = sys.argv[1]
PASSWD = sys.argv[2]

driver = webdriver.Firefox()

"""
    @TO-DO: "Add a string template, add string file with birthday message"
    @TO-DO: "Put this in another script"
    @TO-DO: "Check user gender via genderize API https://api.genderize.io/?name=Daniel"
"""
def format_message(user_name):
    first_name = user_name.split(' ')[0]
    return "Parabens "+first_name+" :D ! Beijinhos"

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
            # @TO-DO[1]: "Missing for loop for each users_name in users_names"
            text_areas = driver.find_element_by_xpath("//div[@class='innerWrap'][1]//textarea[1]")
            text_areas.send_keys(format_message(users_names.text))
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
    date = driver.find_element_by_xpath("//div[@class='fbEventsDashboardSection'][2]")
    i_user_link = 1
    while i_user_link < 3:
        # @TO-DO-REF[1]
        # Imagine a perfect loop birthday write wishes!
        user_name = driver.find_element_by_xpath("//div[@id='events_birthday_view'][1]//a")
        i_user_link = i_user_link + 1
        print user_name
        print user_name.text

# Call main task
# wish_a_happy_birthday()

# Call future birthday's provisionary
print_birthdays_full_report()
