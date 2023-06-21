from selenium import webdriver
import os
import concurrent.futures
import threading
import time
import re

MAX_WORKERS = 10
BOX_XPATH = "/html/body/section/div[3]/div/div[2]"
INFO_XPATH = "/html/body/section/article[1]/div/div/div[2]"
BUILT_WITH_XPATH = "/html/body/section/article[1]/div/div/div[3]/ul"
project_pages: list[str] = [f"https://devpost.com/software/search?page={num}&query=is%3Awinner" for num in range(1, 10)]

def get_projects():
    driver = webdriver.Chrome(options=chrome_options)
    while len(project_pages) > 0:
        page = project_pages.pop()
        driver.get(page)
        links = driver.find_element("xpath", BOX_XPATH).find_elements("tag name", "a")
        project_links = [link.get_attribute("href") for link in links]
        projects.extend(project_links)
    driver.quit()
    print(f"Finished {threading.current_thread().name} with {len(project_pages)} pages left")

def get_info():
    driver = webdriver.Chrome(options=chrome_options)
    while len(projects) > 0:
        page = projects.pop()
        driver.get(page)
        info = [p.text for p in driver.find_element("xpath", INFO_XPATH).find_elements("tag name", "p")]
        built_with = [li.text for li in driver.find_element("xpath", BUILT_WITH_XPATH).find_elements("tag name", "li")]


if __name__ == "__main__":
    start = time.time()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")

    projects = []
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
    pages_futures = [pool.submit(get_projects) for _ in range(MAX_WORKERS)]
    concurrent.futures.wait(pages_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
    print(len(projects), len(project_pages))