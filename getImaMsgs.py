import find_content_of_page
import json


def iterate_page(n: int, target_current_author: str) -> list:
    msgs = []
    #fxp_url = f"https://www.fxp.co.il/showthread.php?t=21780977&page={n}"
    messages_json = find_content_of_page.extract_fx_posts_json(n)

    # Filter posts by current_author
    for post in messages_json:
        if post["current_author"] == target_current_author:
            msgs.append(post)
    return msgs


def main():
    peoples = ["multi400","ImaLele"]
    arr_msgs = []
    for i in range(200, 219):
        arr_msgs += iterate_page(i, peoples[1])

    # Print filtered messages pretty JSON
    print(json.dumps(arr_msgs, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
