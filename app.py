from flask import Flask, jsonify, render_template, send_file, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from yt_dlp import YoutubeDL
import time
from io import BytesIO

app = Flask(__name__)

def get_random_shorts_links():
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.youtube.com/")
        time.sleep(5)

        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys("shorts")
        search_box.submit()
        time.sleep(5)

        filters = driver.find_elements(By.XPATH, "//yt-formatted-string[contains(text(), 'Shorts')]")
        if filters:
            filters[0].click()
            time.sleep(3)

        shorts_links = []
        num_links = 5
        retries = 1

        while len(shorts_links) < num_links and retries < 50:
            try:
                videos = driver.find_elements(By.XPATH, "//a[contains(@href, '/shorts/')]")
                for video in videos:
                    href = video.get_attribute("href")
                    if href and href not in shorts_links:
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(f"https://www.youtube.com/embed/{href.split('/shorts/')[1]}")
                        time.sleep(2)

                        if "Video unavailable" not in driver.page_source:
                            shorts_links.append(href)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                        if len(shorts_links) >= num_links:
                            break

                driver.execute_script("window.scrollBy(0, 1000)")
                time.sleep(3)
            except WebDriverException:
                pass

            retries += 1

        downloadable_links = convert_links_to_downloadable(shorts_links)

        # Save links to files
        save_links_to_file(shorts_links, file_name="links.txt", mode="a")
        save_links_to_file(downloadable_links, file_name="downloadable_links.txt", mode="a")

        return shorts_links

    finally:
        driver.quit()

def get_random_snapchat_reels():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Disable browser notifications
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("unhandledPromptBehavior", "dismiss")  # Dismiss all alerts automatically

    driver = webdriver.Chrome(options=chrome_options)  # Adjust to your WebDriver (e.g., Firefox, Edge, etc.)
    try:
        driver.get("https://www.snapchat.com/spotlight")
        time.sleep(5)  # Wait for page to load

        snapchat_links = []
        num_links = 5
        retries = 1

        while len(snapchat_links) < num_links and retries < 50:
            try:
                reels = driver.find_elements(By.XPATH, "//a[contains(@href, '/spotlight')]")
                for reel in reels:
                    href = reel.get_attribute("href")
                    if href and href not in snapchat_links:
                        snapchat_links.append(href)

                        if len(snapchat_links) >= num_links:
                            break

                driver.execute_script("window.scrollBy(0, 1000)")
                time.sleep(3)
            except WebDriverException:
                pass

            retries += 1

        downloadable_links = convert_links_to_downloadable(snapchat_links)

        # Save links to files
        save_links_to_file(snapchat_links, file_name="links.txt", mode="a")
        save_links_to_file(downloadable_links, file_name="downloadable_links.txt", mode="a")

        return snapchat_links

    finally:
        driver.quit()
        
def get_random_tiktok_reels():
    chrome_options = Options()
    # Remove headless mode to show browser window
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options  # Now shows visible browser
    )

    try:
        driver.get("https://www.tiktok.com/")
        time.sleep(5)

        # Handle cookie popup
        try:
            cookie_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
            cookie_button.click()
            time.sleep(1)
        except WebDriverException:
            pass

        reels_links = []
        num = 5  # Number of TikTok videos to collect
        while len(reels_links) < num:
            driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(3)
            
            # Find all video links
            videos = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
            for video in videos:
                href = video.get_attribute("href")
                if href and href not in reels_links:
                    reels_links.append(href)
                if len(reels_links) >= num:
                    break

        # Generate downloadable URLs through Flask endpoint
        downloadable_links = [
            url_for('download_video', video_url=link, _external=True) 
            for link in reels_links
        ]
        
        # Save to existing files without changing other platforms' data
        save_links_to_file(reels_links, "links.txt", mode="a")
        save_links_to_file(downloadable_links, "downloadable_links.txt", mode="a")

        return reels_links

    finally:
        driver.quit()        

def convert_links_to_downloadable(links):
    ydl_opts = {"quiet": True, "format": "best", "noplaylist": True}
    downloadable_links = []

    with YoutubeDL(ydl_opts) as ydl:
        for link in links:
            try:
                info = ydl.extract_info(link, download=False)
                downloadable_links.append(info["url"])
            except Exception as e:
                print(f"Failed to process {link}: {str(e)}")

    return downloadable_links

def save_links_to_file(links, file_name="links.txt", mode="w"):
    with open(file_name, mode) as file:
        for link in links:
            file.write(link + "\n")
    print(f"Links saved to {file_name}")
    
@app.route('/download/<path:video_url>')
def download_video(video_url):
    try:
        ydl_opts = {
            "quiet": True,
            "format": "best",
            "noplaylist": True,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://www.tiktok.com/",
            },
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_url = info['url']
            response = ydl.urlopen(video_url)
            buffer = BytesIO(response.read())
            buffer.seek(0)
            
            return send_file(
                buffer,
                mimetype=response.headers.get('Content-Type'),
                as_attachment=True,
                download_name=f"{info['title']}.mp4"
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500    

@app.route('/get-links', methods=['GET'])
def get_links():
    try:
        shorts_links = get_random_shorts_links()
        snapchat_links = get_random_snapchat_reels()
        tiktok_links = get_random_tiktok_reels()  # New line

        return jsonify({
            "status": "success",
            "shorts_links": shorts_links,
            "snapchat_links": snapchat_links,
            "tiktok_links": tiktok_links  # New line
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def index():
    try:
        shorts_links = get_random_shorts_links()
        snapchat_links = get_random_snapchat_reels()
        tiktok_links = get_random_tiktok_reels()  # New line
        return render_template(
            'index.html',
            shorts_links=shorts_links,
            snapchat_links=snapchat_links,
            tiktok_links=tiktok_links  # New line
        )
    except Exception as e:
        return f"Error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
