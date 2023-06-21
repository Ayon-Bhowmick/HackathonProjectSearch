from selenium import webdriver
import concurrent.futures
import threading
import time
import os

MAX_WORKERS = 100
NUM_PAGES = 1301
BOX_XPATH = "/html/body/section/div[3]/div/div[2]"
INFO_XPATH = "/html/body/section/article[1]/div/div/div[2]"
BUILT_WITH_XPATH = "/html/body/section/article[1]/div/div/div[3]/ul"
TITLE_XPATH = "/html/body/section/header/div[1]/div/h1"
RESERVED_CHARS = ("<", ">", ":", "\"", "/", "\\", "|", "?", "*")
project_pages: list[str] = [f"https://devpost.com/software/search?page={num}&query=is%3Awinner" for num in range(1, NUM_PAGES + 1)]

def get_projects():
    print(f"Starting {threading.current_thread().name} with {len(project_pages)} pages left")
    driver = webdriver.Chrome(options=chrome_options)
    while len(project_pages) > 0:
        print(f"{len(projects)} pages left")
        page = project_pages.pop()
        driver.get(page)
        links = driver.find_element("xpath", BOX_XPATH).find_elements("tag name", "a")
        project_links = [link.get_attribute("href") for link in links]
        projects.extend(project_links)
    driver.quit()
    print(f"Finished {threading.current_thread().name} with {len(project_pages)} pages left")

def get_info():
    print(f"Starting {threading.current_thread().name} with {len(projects)} projects left")
    driver = webdriver.Chrome(options=chrome_options)
    while len(projects) > 0:
        print(f"{len(projects)} projects left")
        page = projects.pop()
        driver.get(page)
        info = [p.text for p in driver.find_element("xpath", INFO_XPATH).find_elements("tag name", "p")]
        built_with = [li.text for li in driver.find_element("xpath", BUILT_WITH_XPATH).find_elements("tag name", "li")]
        info.append(", ".join(built_with))
        title = driver.find_element("xpath", TITLE_XPATH).text
        # replace all invalid characters with _
        title = "".join([char if char not in RESERVED_CHARS else "_" for char in title])
        with open(f"Projects/{title}.txt", "w") as f:
            f.write("\n".join(info))
    driver.quit()
    print(f"Finished {threading.current_thread().name} with {len(projects)} projects left")



if __name__ == "__main__":
    start = time.time()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")

    projects = []
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
    pages_futures = [pool.submit(get_projects) for _ in range(MAX_WORKERS)]
    concurrent.futures.wait(pages_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
    print(len(projects), len(project_pages))

    while len(projects) > 0:
        print(f"staring new loop with {len(projects)} projects left")
        project_futures = [pool.submit(get_info) for _ in range(MAX_WORKERS)]
        concurrent.futures.wait(project_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
        print(len(os.listdir("Projects")), len(projects))
    pool.shutdown(wait=True)

    seconds = time.time() - start
    minutes = seconds // 60
    seconds = seconds - minutes * 60
    hours = minutes // 60
    minutes = minutes - hours * 60
    print(f"Total time: {int(hours)}:{int(minutes)}:{seconds}")
