import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from utils.constants import (
    EVENTBRITE_BASE_URL,
    EVENT_CARD_SELECTOR,
    OUTPUT_CSV,
    OUTPUT_JSON,
    WAIT_TIME,
)
from utils.helpers import export_to_csv, export_to_json, parse_event_card


def main():
    parser = argparse.ArgumentParser(description="Scrape Eventbrite events")
    parser.add_argument("--pages", type=int, default=10,
                        help="Number of pages to scrape (default: 10)")
    args = parser.parse_args()

    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Scape pages 1 to 10
    events = []
    seen_events = set()
    for page in range(1, args.pages + 1):
        print(f"Scraping page {page}")

        # Navigate to the Eventbrite URL
        url = EVENTBRITE_BASE_URL.format(page=page)
        driver.get(url)
        time.sleep(WAIT_TIME)

        # Find all event cards
        event_cards = driver.find_elements(
            By.CSS_SELECTOR, EVENT_CARD_SELECTOR)

        # Parse each event card
        for event_card in event_cards:
            event_data = parse_event_card(event_card, driver, seen_events)
            if event_data:
                events.append(event_data)

    driver.quit()

    export_to_csv(events, OUTPUT_CSV)
    export_to_json(events, OUTPUT_JSON)


if __name__ == "__main__":
    main()
