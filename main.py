import os
import time
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright

load_dotenv()

def run(playwright: Playwright) -> None:
    message = open("message.txt", "r").read()

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.instagram.com/")
    page.get_by_label("Phone number, username, or").click()
    page.get_by_label("Phone number, username, or").fill(os.getenv("IG_EMAIL"))
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(os.getenv("IG_PASSWORD"))
    page.get_by_role("button", name="Log in", exact=True).click()
    time.sleep(5)
    page.get_by_role("button", name="Not now").click()
    time.sleep(5)
    page.get_by_role("button", name="Not Now").click()

    file = open("usernames.txt", "r")
    usernames = file.readlines()

    for username in usernames:
        username = username.replace("\n", "")
        page.goto(f"https://www.instagram.com/{username}/")
        time.sleep(5)
        page.get_by_role("button", name="Message").click()
        time.sleep(2)
        page.get_by_label("Message", exact=True).press("ControlOrMeta+-")
        page.get_by_label("Message", exact=True).fill(message)
        page.keyboard.press("Enter")
        time.sleep(2)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)