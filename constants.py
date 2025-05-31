# Scraping Constants
EVENTBRITE_BASE_URL = "https://www.eventbrite.com/d/singapore--singapore/all-events/?page={page}"
WAIT_TIME = 3
URGENCY_KEYWORDS = {
    "almost full",
    "going fast",
    "sales end soon",
    "just added"
}

# CSS Selectors
EVENT_CARD_SELECTOR = "section.event-card-details"
TITLE_SELECTOR = "a.event-card-link h3"
ANCHOR_SELECTOR = "a.event-card-link"
P_TAG_SELECTOR = "p"

# Attribute Names
ATTR_HREF = "href"
ATTR_LOCATION = "data-event-location"
ATTR_PAID_STATUS = "data-event-paid-status"
ATTR_CATEGORY = "data-event-category"

# Output Files
OUTPUT_CSV = "data/eventbrite.csv"
OUTPUT_JSON = "data/eventbrite.json"
