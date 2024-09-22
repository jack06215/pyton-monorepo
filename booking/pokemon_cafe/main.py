import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from booking.definition import ROOT_DIR


def parse_calendar_text(text: str) -> None:
    # Get Current month
    current_month_pattern = r"\d{4}年\d{1,2}月"

    # Split the string using regex
    current_month: str = re.findall(current_month_pattern, text)[0]
    print(current_month)

    # Regex pattern to split after the Saturday
    after_sat = r"土[\s\S]*?"
    day_of_month: str = re.split(after_sat, text, 1)[1]

    # Split based on the pattern that matches the digit "1"
    split_string = re.split(
        r"(?<=\b1\b)",
        day_of_month,
    )
    first_day_of_month: list[str] = split_string[0].splitlines()
    rest_of_days: list[str] = split_string[1].splitlines()
    rest_of_days = rest_of_days[0:-1]  # Remove the "1" at the end

    all_days = first_day_of_month + rest_of_days
    all_days = list(filter(lambda x: x != "", all_days))

    if len(all_days) == 0:
        return

    for i in range(len(all_days)):
        if all_days[i].isnumeric():
            if all_days[min(i + 1, len(all_days) - 1)] == "満席":
                print(f"{all_days[i]} is {all_days[i + 1]}")
                continue

            if int(all_days[i]) > 31:
                continue

            print(all_days[i])


def create_booking(location: str, n_guests: int) -> None:
    if location == "Tokyo":
        website = "https://reserve.pokemon-cafe.jp/"
    elif location == "Osaka":
        website = "https://osaka.pokemon-cafe.jp/"

    chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    service = Service(executable_path=f"{ROOT_DIR}/chromedriver.exe")
    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.get(website)
    try:
        # Step 1: Agree to terms and conditions
        driver.find_element(
            By.XPATH,
            "//*[@class='agreeChecked']",
        ).click()
        driver.find_element(
            By.XPATH,
            "//*[@class='button']",
        ).click()

        # Step 2: Make reservation button
        make_reservation_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@class='button arrow-down']")
            )
        )
        make_reservation_button.click()

        # Step 3: Fill in number of people
        select = Select(driver.find_element(By.NAME, "guest"))
        select.select_by_index(n_guests)

        # Step 4: Reads calendar and find available dates
        calendar_element = driver.find_element(
            By.XPATH,
            "//*[@id='step2-form']/div",
        )
        parse_calendar_text(calendar_element.text)

    except NoSuchElementException:
        pass

    except Exception as e:
        raise Exception(f"Failed to book for Tokyo: {e}")

    finally:
        print("Booking process completed.")


def main() -> None:
    create_booking("Tokyo", 1)


if __name__ == "__main__":
    main()
