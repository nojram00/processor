from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from db import save_log

HOST_URL = "https://my-fucking-service.onrender.com"


def fetch_and_modify_video():
    # fetch data (Get only view count):
    try:
        response = requests.get(f"{HOST_URL}/get-video-info")

        response.raise_for_status()

        data = response.json()

        if not data["items"]:
            print("No Video Found...")
            return

        info = data['items'][0]

        view_count = info['statistics']['viewCount']

        print(f"This video has {view_count} view/s")

        update_video_title(f"This video has {view_count} views")

    except Exception as e:
        print(f"Error: {e}")


def update_video_title(title : str):

    data = {
            "title" : title,
            "description" : "No Description kase tamad ako",
            "tags" : "None"
        }
    try:
        response = requests.post(f"{HOST_URL}/update-video", json=data)

        response.raise_for_status()

        save_log(f"Title updated: '{data['title']}'")


    except Exception as e:
        print(f"Error: {e}")


print("Running....")

def run_dummy(port):
    httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

scheduler = BackgroundScheduler()

scheduler.add_job(fetch_and_modify_video, 'interval', hours=12, max_instances=3)

scheduler.start()

run_dummy(8000)

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()


