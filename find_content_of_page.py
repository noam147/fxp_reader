import requests
from bs4 import BeautifulSoup
import re
import json

def __get_username(post_div):
    username_tag = post_div.find_previous("a", class_="bigusername")
    if username_tag and username_tag.text.strip():
        return username_tag.text.strip()
    username_tag2 = post_div.find_previous("a", class_="username")
    if username_tag2:
        span_nick = username_tag2.find("span", class_="user_nick_s1")
        if span_nick and span_nick.text.strip():
            return span_nick.text.strip()
        strong_tag = username_tag2.find("strong")
        if strong_tag and strong_tag.text.strip():
            return strong_tag.text.strip()
        return username_tag2.text.strip()
    return "Unknown"

def extract_fx_posts_json(n):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.fxp.co.il/showthread.php?t=21780977&page={n}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    posts = []

    for post_div in soup.find_all("div", id=re.compile(r"post_message_\d+")):
        curr_author = __get_username(post_div)

        quoted_author = ""
        quoted_content = ""

        quote_block = post_div.find("div", class_="bbcode_quote")
        if quote_block:
            quote_author_tag = quote_block.find("strong")
            quote_msg_tag = quote_block.find("div", class_="message")
            if quote_author_tag and quote_msg_tag:
                quoted_author = quote_author_tag.text.strip()
                quoted_content = quote_msg_tag.get_text(separator="\n", strip=True)

        for q in post_div.find_all("div", class_="bbcode_quote"):
            q.decompose()

        main_msg = post_div.get_text(separator="\n", strip=True)

        posts.append({
            "page":n,
            "quoted_author": quoted_author,
            "quoted_content": quoted_content,
            "current_author": curr_author,
            "current_message": main_msg
        })

    return posts


