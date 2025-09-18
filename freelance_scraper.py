
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.service import Service
from telegram import Bot



TOKEN = "7800854300:AAFHc4dPf25BboyL0q0iCp6AK6fH6QLTyvU"
users_id = ["717613461"]
infor = ["scrap", "script", "pdf"]

def scraping():
    service = Service("chromedriver.exe")
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(7)

    wait = WebDriverWait(driver, 4000)
    all_info = []
    driver.get("https://www.freelancer.com/login")
    email = wait.until(expected_conditions.presence_of_element_located((By.ID, "emailOrUsernameInput")))
    email.send_keys("rekatartem@gmail.com")
    password = wait.until(expected_conditions.presence_of_element_located((By.ID, "passwordInput")))
    password.send_keys("coffeeyok1")

    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,
                                                    "//button[contains(text(), 'Log in')]"))).click()

    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,
                                                    "//button[contains(text(), 'No, thanks')]"))).click()
    wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "ModalCloseButton"))).click()

    wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(., Browse)]"))).click()
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,
                                                            "//app-browse-links-item[contains(., Projects)]"))).click()

    while True:
        stop = find_element(all_info, driver)
        if stop:
            break
        next_list(driver, wait)
    driver.quit()
    return all_info

def find_element(all_info, driver):
    all_projects = driver.find_elements(By.CSS_SELECTOR, "a[fltrackinglabel=RedirectToPVP]")
    print(len(all_projects))
    for project in all_projects:
        title = project.find_element(By.CSS_SELECTOR, 'fl-heading[class="Title-text"]')
        print(title.text)
        data = project.find_element(By.CSS_SELECTOR, "fl-relative-time")
        print(data.text)
        link = project.get_attribute('href')
        print(link)
        for info in infor:
            if info in title.text.lower():
                all_info.append([title.text, data.text, link])

        if data.text.strip() == "1 day":
            return True
        print(title.text, data.text, link)
    print("----------------")
    return False

def next_list(driver, wait):
    next_page = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                    "button[aria-label='Next page']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", next_page)

    time.sleep(2)
    driver.execute_script("arguments[0].click();", next_page)


async def send_to_telegram():
    messages = scraping()
    bot = Bot(token=TOKEN)
    for user in users_id:
        for info in messages:
            text = f"{info[0]}\n🕒{info[1]}\n{info[2]}"
            await bot.send_message(chat_id=user, text=text)
            await asyncio.sleep(1)



if __name__ == "__main__":
    asyncio.run(send_to_telegram())
