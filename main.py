import os
from dotenv import load_dotenv
import urllib.request
import urllib.error
import json
import sys

load_dotenv()
API_TOKEN = os.getenv("HETZNER_API_KEY")
SERVER_ID = os.getenv("HETZNER_SERVER_ID")


if not API_TOKEN or not SERVER_ID:
    print("Error: HETZNER_API_TOKEN and HETZNER_SERVER_ID must be set.")
    sys.exit(1)

TB = 1024**4
GB = 1024**3
SHUTDOWN_THRESHOLD_BYTES = 19 * TB


url = f"https://api.hetzner.cloud/v1/servers/{SERVER_ID}"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP Error fetching server data: {e.code} {e.reason}")
    sys.exit(1)
except Exception as e:
    print(f"Error fetching server data: {e}")
    sys.exit(1)

server = data.get("server", {})
status = server.get("status", "unknown")
outgoing_traffic = server.get("outgoing_traffic") or 0

print(f"Current outgoing traffic: {outgoing_traffic / GB:.2f} GB")

if status == "running":
    if outgoing_traffic >= SHUTDOWN_THRESHOLD_BYTES:
        print("19 TB limit reached. Sending shutdown request...")
        try:
            shutdown_req = urllib.request.Request(f"{url}/actions/shutdown", method='POST', headers=headers)
            with urllib.request.urlopen(shutdown_req) as response:
                print("Shutdown request sent successfully.")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error during shutdown: {e.code} {e.reason}")
        except Exception as e:
            print(f"Error during shutdown: {e}")
    else:
        print("Server running, but under 19 TB. No action taken.")
else:
    print(f"Server is not running (status: {status})")
