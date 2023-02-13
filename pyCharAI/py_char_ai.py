import time
import asyncio
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import WebElement

tag = '[pyCharAI]:'

# Main page
btn_send = (By.XPATH, '//*[name()="button"][@class="btn py-0"]')
btn_send_disabled = (By.XPATH, '//*[name()="button"][@class="btn py-0"][@disabled]')
tbox_message = (By.XPATH, '//*[@id="user-input"]')
p_responses = (
    By.XPATH,
    '//*[name()="div"][@class="markdown-wrapper markdown-wrapper-last-msg swiper-no-swiping"]/*/*[name()="p"]')

# Login page
btn_welcome = (By.ID, "#AcceptButton")
btn_go_to_login = (By.XPATH, '//*[@class=" btn border"]')
tbox_email = (By.ID, 'username')
tbox_password = (By.ID, 'password')
btn_continue = (By.XPATH, '//div[@class="c3082a2a5"]/button')
a_profile = (By.XPATH, '//*[@href="/profile?"]')


class PyCharAI:
    def __init__(self, character_id, email, password):
        options = uc.ChromeOptions()
        options.headless = True
        self.driver = uc.Chrome(options)
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=.2)

        self.__url = f"https://beta.character.ai/chat?char={character_id}"
        self.__credentials = (email, password)
        self.__init_browser()

    def __authenticate_browser(self):

        # Wait until site loads and go to the login page
        self.driver.get('https://beta.character.ai/login')
        print(tag, 'Initialized authentication sequence.')
        btn = self.wait.until(EC.presence_of_element_located(btn_welcome))
        self.wait.until(EC.element_to_be_clickable(btn_welcome))
        btn.click()
        btn = self.wait.until(EC.presence_of_element_located(btn_go_to_login))
        self.wait.until(EC.element_to_be_clickable(btn_go_to_login))
        btn.click()
        print(tag, 'Login page seems astounding..')

        # Send the keystrokes to the login page
        email = self.wait.until(EC.presence_of_element_located(tbox_email))
        email.send_keys(self.__credentials[0])
        password = self.wait.until(EC.presence_of_element_located(tbox_password))
        password.send_keys(self.__credentials[1])
        btn = self.wait.until(EC.presence_of_element_located(btn_continue))

        print(tag, 'Sending credentials...')
        btn.click()

        # Check if user is logged
        self.wait.until(EC.presence_of_element_located(a_profile))
        print(tag, 'Logged in....')
        del self.__credentials

    def __init_browser(self):

        # Authorize the browser
        self.__authenticate_browser()
        self.driver.get(self.__url)
        self.wait.until(EC.presence_of_element_located(p_responses))
        print('READY')

    def ask(self, question):
        # Sends the keystrokes and presses the send button
        tbox_input = self.wait.until(EC.presence_of_element_located(tbox_message))
        tbox_input.send_keys(question)
        btn: WebElement = self.wait.until(EC.presence_of_element_located(btn_send))
        self.wait.until(EC.element_to_be_clickable(btn_send))
        btn.click()

        # Awaits the response
        event = False
        while not event:
            if btn.is_enabled():
                event = True
            else:
                time.sleep(.2)

        responses = self.wait.until(EC.presence_of_all_elements_located(p_responses))
        f_response = ''
        for response in responses:
            f_response += response.text + '\n'
        return f_response

    # noinspection PyBroadException
    async def ask_async(self, question):
        # Sends the keystrokes and presses the send button
        tbox_input = self.wait.until(EC.presence_of_element_located(tbox_message))
        tbox_input.send_keys(question)
        btn: WebElement = self.wait.until(EC.presence_of_element_located(btn_send))
        self.wait.until(EC.element_to_be_clickable(btn_send))
        btn.click()

        # Awaits the response
        event = asyncio.Event()
        while not event.is_set():
            if btn.is_enabled():
                event.set()
            else:
                await asyncio.sleep(.2)

        responses = self.wait.until(EC.presence_of_all_elements_located(p_responses))
        f_response = ''
        for response in responses:
            f_response += response.text + '\n'
        return f_response
