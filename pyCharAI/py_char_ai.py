import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebElement

accept_button = (By.ID, "#AcceptButton")
send_button = (By.XPATH, "")


class PyCharAI:
    def __init__(self, url, cookies):
        self.driver = uc.Chrome()
        self.__url = url
        self.__cookies = cookies

        self.__init_browser()

    def __init_browser(self):
        # Sets the cookies
        for name, value in self.__cookies.items():
            self.driver.execute_cdp_cmd(
                'Network.setCookie',
                {
                    'domain': 'beta.character.ai',
                    'path': '/',
                    'name': name,
                    'value': value,
                    'httpOnly': True,
                    'secure': True,
                },
            )
        # Gets the website
        self.driver.get(self.__url)

        # Raises timeout exception if it can't access the site after 10 seconds
        button: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(accept_button)
        )
        button.click()

    def ask(self, question):
        return
