import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from utils.constants import (
    ANCHOR_SELECTOR,
    ATTR_CATEGORY,
    ATTR_HREF,
    ATTR_LOCATION,
    ATTR_PAID_STATUS,
    P_TAG_SELECTOR,
    TITLE_SELECTOR,
    URGENCY_KEYWORDS,
)


def parse_event_card(event: WebElement, driver: WebDriver, seen_events: set[str]) -> dict[str, str] | None:
    """
    Parse the event card and return a dictionary of the event data.

    Note: Title and <p> tags require JavaScript extraction via innerText due to dynamic rendering issues.
    """
    try:
        # 1. Title
        title_elem = event.find_element(
            By.CSS_SELECTOR, TITLE_SELECTOR)
        title = driver.execute_script(
            "return arguments[0].innerText;", title_elem).strip()

        # Check if the event has already been scraped
        if title in seen_events:
            return None

        seen_events.add(title)

        # 2. URL and associated metadata
        anchor = event.find_element(By.CSS_SELECTOR, ANCHOR_SELECTOR)
        url = anchor.get_attribute(ATTR_HREF)
        location = anchor.get_attribute(ATTR_LOCATION)
        paid_status = anchor.get_attribute(ATTR_PAID_STATUS)
        category = anchor.get_attribute(ATTR_CATEGORY)

        # 3. <p> tags for additional data
        p_tags = event.find_elements(By.TAG_NAME, P_TAG_SELECTOR)
        texts = [driver.execute_script(
            "return arguments[0].innerText;", p).strip() for p in p_tags]

        urgency = date_time = price = host = None

        for text in texts:
            lower = text.lower()
            if lower in URGENCY_KEYWORDS:
                urgency = text
            elif "am" in lower or "pm" in lower:
                date_time = text
            elif "$" in text:
                price = text
            else:
                host = text

        # 4. Consolidate data
        event_data = {}
        event_data["Title"] = title
        event_data["URL"] = url
        event_data["Location"] = location
        event_data["Paid Status"] = paid_status
        event_data["Category"] = category
        event_data["Urgency"] = urgency
        event_data["Date & Time"] = date_time
        event_data["Price"] = price
        event_data["Host"] = host

        return event_data

    except Exception as e:
        print(f"Failed to parse event: {e}")
        return None


def export_to_csv(events: list[dict[str, str]], filename: str) -> None:
    df = pd.DataFrame(events)
    df.to_csv(filename, index=False, encoding='utf-8')


def export_to_json(events: list[dict[str, str]], filename: str) -> None:
    df = pd.DataFrame(events)
    df.to_json(filename, orient='records', indent=4)
