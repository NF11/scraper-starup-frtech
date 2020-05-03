import itertools
import sys
import time

DONE = False


def _french_login(driver):
    driver.implicitly_wait(100)
    driver.find_element_by_css_selector("button.button.login-button").click()
    driver.find_element_by_id('email').send_keys('orion.ashten@iillii.org')
    driver.find_element_by_id('password').send_keys('123456email')
    driver.find_element_by_css_selector('button.button.dark-button.button-large.button-loader.login-button').click()
    driver.refresh()
    driver.implicitly_wait(500)
    print('refrech')


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if DONE:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


