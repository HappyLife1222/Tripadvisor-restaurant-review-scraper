# TripAdvisor Restaurant Review Scraper

This project is a Python script that scrapes restaurant reviews from TripAdvisor. It uses Selenium with undetected_chromedriver to navigate the website and BeautifulSoup to parse the HTML. The script is designed to handle captchas and cookies, and it can scroll to the bottom of pages to load more content.

## Features

- Scrapes restaurant reviews including restaurant name, username, rating, and description.
- Handles captchas by restarting the script.
- Handles cookies by accepting them.
- Scrolls to the bottom of pages to load more content.
- Writes scraped data to a CSV file.
- Removes duplicate entries from the CSV file.
- Sorts the CSV file by restaurant name.

## How to Use

1. Clone this repository.
2. Install the required Python packages: `undetected_chromedriver`, `beautifulsoup4`, `selenium`.
3. Run the script with `python main.py`.
4. When prompted, enter the number of restaurants you want to scrape.

The script will start scraping reviews and write them to a CSV file named `reviews.csv`. If a captcha is triggered, the script will pause for a few seconds and then restart. The script will also scroll to the bottom of pages to load more content.

## Limitations

This script is intended for educational purposes only. Please respect TripAdvisor's terms of service and do not use this script for large-scale scraping.

## License

This project is licensed under the MIT License.