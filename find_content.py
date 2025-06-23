import requests
from bs4 import BeautifulSoup
import re

def extract_fx_posts(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    posts = []

    # Find all post_message_ elements
    post_divs = soup.find_all("div", id=re.compile(r"post_message_\d+"))

    for div in post_divs:
        # Get the inner text, including quotes
        text = div.get_text(separator="\n", strip=True)
        posts.append(text)

    return posts

# Example usage:
fxp_url = "https://www.fxp.co.il/showthread.php?t=21780977&page=217"
messages = extract_fx_posts(fxp_url)

for i, msg in enumerate(messages, 1):
    print(f"--- Post {i} ---\n{msg}\n")
