import time
import httpx


def get_dummy():
    url = "http://127.0.0.1:8000/dummy"
    with httpx.Client() as client:
        r = client.get(url, timeout=5.0)
        r.raise_for_status()
        print(r.json())


if __name__ == "__main__":
    # small delay if server is starting in same session
    time.sleep(1)
    try:
        get_dummy()
    except Exception as e:
        print("Request failed:", e)
