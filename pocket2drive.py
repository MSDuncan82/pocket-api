import requests
import json
import dotenv
import os
import glob
import time
import sys
import argparse
from chrome_print import print_pdfs
from sync import sync_dir

dotenv.load_dotenv()
sys.path.append(".")


def get_content(since, api_endpoint="https://getpocket.com/v3/get"):

    params = dict(
        consumer_key=os.environ["CONSUMER_KEY"],
        access_token=os.environ["ACCESS_TOKEN"],
        state="all",
        detailType="simple",
        contentType="article",
        since=since,
    )

    response = requests.get(api_endpoint, params=params)

    return response.json()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", "-r", default=False, action="store_true")
    args = parser.parse_args()

    proj_dir = os.path.abspath(os.path.dirname(__file__))

    since_path = f"{proj_dir}/since.txt"
    if args.reset:
        os.remove(since_path)
        existing_files = glob.glob("/home/mike/googledrive/reMarkable/*")
        [os.remove(f) for f in existing_files]

    current_time = int(time.time())
    try:
        lines = open(since_path, "r").readlines()
        since = int(lines[-1])
    except FileNotFoundError:
        since = 0
    finally:
        with open(since_path, "a+") as f:
            f.write("\n")
            f.write(f"{current_time}")

    response_json = get_content(since)
    content = response_json["list"]
    rm_path = os.environ["RM_PATH"]

    if content:
        url_list = [resource["resolved_url"] for resource in content.values()]
        print_pdfs(url_list)

    print(f"Printed {len(url_list)} articles from pocket")

    print(f"Syncing...")

    sync_dir()
