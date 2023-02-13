import time
import asyncio
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

tag = '[pyCharAI]:'

# Main page
btn_send = (By.XPATH, '//*[name()="button"][@class="btn py-0"]')
tbox_message = (By.XPATH, '//*[@id="user-input"]')
p_responses = (
    By.XPATH,
    '//*[name()="div"][@class="markdown-wrapper markdown-wrapper-last-msg swiper-no-swiping"]/*/*[name()="p"]'
)

# Login page
btn_welcome = (By.ID, "#AcceptButton")
btn_go_to_login = (By.XPATH, '//*[@class=" btn border"]')
tbox_email = (By.ID, 'username')
tbox_password = (By.ID, 'password')
btn_continue = (By.XPATH, '//button[text()="Continue"]')
a_profile = (By.XPATH, '//*[@href="/profile?"]')


class PyCharAI:

    def __init__(self,
                 character_id=None,
                 email=None,
                 password=None,
                 verbose=True):
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            self.driver = uc.Chrome(
                options=options
            )
        except TypeError as e:
            if str(
                    e
            ) == 'expected str, bytes or os.PathLike object, not NoneType':
                raise ValueError('Chrome installation not found')
            raise e
        self.wait = WebDriverWait(self.driver, 20, poll_frequency=.2)
        self.__verbose = verbose
        self.__url = f"https://beta.character.ai/chat?char={character_id}"
        self.__credentials = (email, password)
        self.__init_browser()

    def log(self, prompt):
        if self.__verbose is True:
            print(tag, prompt)

    def __authenticate_browser(self):

        # Wait until site loads and go to the login page
        self.driver.get('https://beta.character.ai/login')
        self.log('Initialized authentication sequence.')
        self.wait.until(EC.element_to_be_clickable(btn_welcome)).click()
        self.wait.until(EC.element_to_be_clickable(btn_go_to_login)).click()
        self.log('Login page seems astounding..')

        # Send the keystrokes to the login page
        self.wait.until(EC.presence_of_element_located(tbox_email)).send_keys(
            self.__credentials[0])
        self.wait.until(
            EC.presence_of_element_located(tbox_password)).send_keys(
                self.__credentials[1])
        self.wait.until(EC.presence_of_element_located(btn_continue)).click()
        self.log('Sending credentials...')

        # Check if user is logged
        self.wait.until(EC.presence_of_element_located(a_profile))
        self.log('Logged in....')
        del self.__credentials

    def __init_browser(self):
        # Authorize the browser
        self.__authenticate_browser()
        self.driver.get(self.__url)
        self.wait.until(EC.presence_of_element_located(p_responses))
        self.log('READY')

    def ask(self, question):
        # Sends keystrokes and presses the send button
        self.wait.until(
            EC.presence_of_element_located(tbox_message)).send_keys(question)
        btn = self.wait.until(EC.element_to_be_clickable(btn_send))
        btn.click()

        # Awaits the response
        event = False
        while not event:
            if btn.is_enabled():
                event = True
            else:
                time.sleep(.2)

        # Returns all the paragraphs separated with newline
        return '\n'.join([
            x.text for x in self.wait.until(
                EC.presence_of_all_elements_located(p_responses))
        ])

    async def ask_async(self, question):
        # Sends keystrokes and presses the send button
        self.wait.until(
            EC.presence_of_element_located(tbox_message)).send_keys(question)
        btn = self.wait.until(EC.element_to_be_clickable(btn_send))
        btn.click()

        # Awaits the response
        event = asyncio.Event()
        while not event.is_set():
            if btn.is_enabled():
                event.set()
            else:
                await asyncio.sleep(.2)

        # Returns all the paragraphs separated with newline
        return '\n'.join([
            x.text for x in self.wait.until(
                EC.presence_of_all_elements_located(p_responses))
        ])
