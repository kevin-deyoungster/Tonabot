import threading
from datetime import datetime
from notify_lib import show_notification
from scraper_lib import search_for

# Set the last checked stamp to 1970....
LAST_CHECKED = datetime.strptime("1 Jan 12:00 am", "%d %b %I:%M %p")
WAIT_TIME_SECONDS = 50
WAIT_TIME_BETWEEN_NOTIFICATIONS = 20


def run(product_name, interval, filter_name=None):
    """
    Entry Point of Tonabot: Runs the scraping function to get new ads for a product every set interval (seconds)

    Parameters:
    product_name (str): The product to search for
    interval (int): The number of seconds to wait before checking again
    filter_name (str): Get only ads with this in their titles
    """
    global LAST_CHECKED

    threading.Timer(interval, run, [product_name, interval]).start()

    ads = []
    try:
        ads = search_for(product_name, LAST_CHECKED, filter_name)
    except AttributeError as error:
        print(f"Error: Could not extract ads from page \n {error}")

    if len(ads) == 0:
        print("No ads found")
    else:
        print(f"{len(ads)} ads found")
        for ad in ads:
            print(f"{ad['name']} - {ad['price']}")
            information = ad["price"] + "\n" + ad["name"]
            show_notification("Tonabot!", information, WAIT_TIME_BETWEEN_NOTIFICATIONS)

    # Update last checked to prevent duplicate notifications
    LAST_CHECKED = datetime.now()


if __name__ == "__main__":
    run("iphone 8", WAIT_TIME_SECONDS, "iphone")
