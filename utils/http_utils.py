import time
import requests


def request_with_retry(url, headers, retries=3, backoff_factor=2):
    delay = 1.0

    for i in range(retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            print(f"Rate limited (429) on {url}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= backoff_factor
            continue
        return response
    return response