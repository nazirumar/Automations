from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')

# Wait for the user to scan the QR code (adjust the sleep time if needed)
time.sleep(20)

def scrape_messages(chat_name):
    # Locate the chat by name and click to open it
    chat = driver.find_element(By.XPATH, f'//*[@id="pane-side"]/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/span/text({chat_name}')
    chat.click()
    time.sleep(3)

    # Locate the message container
    message_container = driver.find_element(By.XPATH, '//div[@class="_1Gy50"]')

    # Scroll up to load older messages
    for _ in range(10):  # Adjust the range for more scrolling
        driver.execute_script("arguments[0].scrollTop = 0;", message_container)
        time.sleep(2)
    # Scrape the messages
    messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')
    for message in messages:
        try:
            text = message.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]/span').text
            print(text)
        except:
            pass

# Replace 'Friend's Name' with the name of the chat you want to scrape
scrape_messages("My-Wife 💞💕")

# Close the driver
# driver.quit()
