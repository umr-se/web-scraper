# Web Scraper

Web Scraper is a Selenium-based backend script built with Flask that scrapes Shorts and Reels from Snapchat, YouTube, and TikTok. The script extracts downloadable links for downloading and watchable links for viewing the scraped content.

## Features
- Scrapes Shorts and Reels from:
  - Snapchat
  - YouTube
  - TikTok
- Extracts and stores:
  - Downloadable links for easy access
  - Watchable links for direct viewing
- Built using Flask and Selenium

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Google Chrome and ChromeDriver (for Selenium)

### Clone the Repository
```sh
git clone https://github.com/umr-se/web-scraper.git
cd web-scraper
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage

### Run the Flask Server
```sh
python app.py
```

### API Endpoints
| Method | Endpoint | Description |
|--------|-------------|---------------------------|
| GET    | `/scrape/snapchat` | Scrape Snapchat Reels |
| GET    | `/scrape/youtube`  | Scrape YouTube Shorts |
| GET    | `/scrape/tiktok`   | Scrape TikTok Reels |

### Example Request
```sh
curl Running on http://127.0.0.1:5000
```
![image](https://github.com/user-attachments/assets/bbb76bc1-7944-4e2d-bc33-77de73b39fe5)

## Configuration
(Optional) Modify the `.env` file to set up Selenium WebDriver and other configurations:
```env (optional)
CHROMEDRIVER_PATH=/path/to/chromedriver
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
For any issues, contact me on [linkedIn] or (https://github.com/umr-se/web-scraper/issues)

![image](https://github.com/user-attachments/assets/f1404ee2-9a5f-475c-b24f-0b8be4c30979)
![image](https://github.com/user-attachments/assets/5048e8b2-ed9d-435f-a4cd-b06cc12ff188)


