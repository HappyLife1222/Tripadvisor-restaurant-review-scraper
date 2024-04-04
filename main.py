import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import random
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def is_captcha(html):
    if "<title>tripadvisor.com.tr</title>" in html:
        print("Captcha triggered")
        return True
    return False


def remove_duplicates(csv_file_name):
    rows = []
    with open(csv_file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(tuple(row))

    rows = list(set(rows))

    with open(csv_file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def sort_by_restaurant_name(csv_file_name):
    with open(csv_file_name, "r") as f:
        reader = csv.reader(f)
        sortedlist = sorted(reader, key=lambda row: row[0], reverse=False)
    with open("reviews.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Restaurant Name", "Username", "Rating", "Description"])
        writer.writerows(sortedlist)


def bottom_page(driver):
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        print(f"Could not scroll to the bottom: {e}")


def get_urls(soup):
    divs = soup.find_all("div", class_=["THBFE", "f", "e"])
    urls = set()
    for div in divs:
        a_tags = div.find_all("a")
        for a in a_tags:
            url = a.get("href")
            if url is not None and url.startswith("/Restaurant_Review"):
                url = url.replace("#REVIEWS", "")
                urls.add(url)
    for url in urls:
        print(url)
    with open("urls.txt", "a") as f:
        for url in urls:
            f.write(url + "\n")


def get_reviews(soup):
    time.sleep(1)
    for x in range(11):
        try:
            restaurant_name = soup.find(
                "h1", attrs={"data-test-target": "top-info-header"}
            ).text
        except:
            restaurant_name = "No restaurant name"
        try:
            rating_span = soup.find_all("span", class_="ui_bubble_rating")[x]
            class_name = rating_span.get("class")[1]
            rating = class_name.split("_")[-1]
        except:
            rating = "No rating"
        try:
            username = soup.find_all("div", class_="info_text pointer_cursor")[x].text
        except:
            username = "Anonymous"
        try:
            description = soup.find_all("p", class_="partial_entry")[x].text.replace(
                "\n", ""
            )
        except:
            description = "No description"
        with open("reviews.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([restaurant_name, username, rating, description])
        print("Review Number:", x)


def restaurant_count():
    try:
        input0 = int(input("How many restaurants do you want to scrape? "))
    except ValueError:
        print("Please enter a valid number")
        restaurant_count()
    return input0

def main():

    with open("urls.txt", "w") as f:
        f.write("")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=118, headless=True)
    url = "https://www.tripadvisor.com.tr"
    driver.get(url)
    time.sleep(1)
    html = driver.execute_script("""return document.documentElement.outerHTML""")
    if is_captcha(html):
        driver.quit()
        time.sleep(random.randint(3, 7))
        main()
    try:
        cookie_accept = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_accept.click()
        time.sleep(0.5)
    except Exception as e:
        print(f"Could not click on the button: {e}")
    try:
        input_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input.hUpcN._G.G_.B-.z.F1._J.w.Cj.R0.NBfGt.H3")
            )
        )
        input_button.click()
        time.sleep(0.5)
    except Exception as e:
        print(f"Could not click on the button: {e}")
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input.hUpcN._G.G_.B-.z.F1._J.w.Cj.R0.FjKFQ.NBfGt.H3")
            )
        )
        input_field.send_keys("London")
        time.sleep(0.5)
    except Exception as e:
        print(f"Could not click on the button: {e}")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a.GzJDZ.w.z._S._F.Wc.Wh.Q.B-._G")
            )
        )
        restoran_buttons = driver.find_elements(
            By.CSS_SELECTOR, "a.GzJDZ.w.z._S._F.Wc.Wh.Q.B-._G"
        )
        for button in restoran_buttons:
            href = button.get_attribute("href")
            if href.startswith(
                "https://www.tripadvisor.com.tr/Restaurants-g186338-London"
            ):
                button.click()
                break
        time.sleep(0.5)
    except Exception as e:
        print(f"Could not click on the button: {e}")

    time.sleep(3)
    bottom_page(driver)
    time.sleep(2)
    html = driver.execute_script("""return document.documentElement.outerHTML""")

    soup = BeautifulSoup(html, "html.parser")
    get_urls(soup)
    pages = [
        "oa30-",
        "oa60-",
        "oa90-",
        "oa120-",
    ]
    url = driver.current_url
    if not url.startswith("https://www.tripadvisor.com.tr/Restaurants-g186338-London"):
        print("URL is not valid")
        driver.quit()
        time.sleep(random.randint(2, 5))
        print("Restarting...")
        main()

    for page in pages:
        insert_index = url.index("g186338-") + len("g186338-")
        url = url[:insert_index] + page + url[insert_index:]
        driver.get(url)
        bottom_page(driver)
        time.sleep(3)
        html = driver.execute_script("""return document.documentElement.outerHTML""")
        if is_captcha(html):
            driver.quit()
            time.sleep(random.randint(2, 5))
            main()
        soup = BeautifulSoup(html, "html.parser")
        get_urls(soup)
    for x in range(input0):
        place = random.choice(open("urls.txt").readlines())
        url = f"https://www.tripadvisor.com.tr{place}"
        review_pages = [
            "",
            "or10-",
            "or20-",
            "or30-",
            "or40-",
            "or50-",
            "or60-",
            "or70-",
            "or80-",
            "or90-",
        ]
        for review_page in review_pages:
            base_url = url
            if "Reviews-" in base_url:
                insert_index = base_url.index("Reviews-") + len("Reviews-")
                url = base_url[:insert_index] + review_page + base_url[insert_index:]
            else:
                print("Substring 'Reviews-' not found in the URL")
                print("Passing to the next restaurant")
                break
            driver.get(url)
            bottom_page(driver)
            expand_buttons = driver.find_elements(
                By.CSS_SELECTOR, "span.taLnk.ulBlueLinks"
            )
            for expand_button in expand_buttons:
                try:
                    expand_button.click()
                    time.sleep(0.5)
                except Exception as e:
                    pass
            time.sleep(2)
            html = driver.execute_script(
                """return document.documentElement.outerHTML"""
            )
            soup = BeautifulSoup(html, "html.parser")
            get_reviews(soup)
            print("Page Number:", review_page)
            time.sleep(random.randint(2, 5))
        print("Restaurant Number:", x + 1)
        remove_duplicates("reviews.csv")
        sort_by_restaurant_name("reviews.csv")
        time.sleep(random.randint(2, 5))
    driver.quit()


if __name__ == "__main__":
    input0 = restaurant_count()
    main()
