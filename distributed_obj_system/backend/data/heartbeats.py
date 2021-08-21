import time
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from utils.const import PORT
from utils.utils import recordHeartbeat, getDataServers, getValidServers
import requests


def sendHeartbeats(interval=60):
   while True:
      for url in getDataServers():
         try:
            res = requests.post(f"http://{url}:{PORT}/heartbeat", timeout=1)
            if res.status_code==200:
                recordHeartbeat(url)
            else:
                print(f"Something wrong with url: {url} with status_code: {res.status_code}", flush=True)
         except Exception as e:
            print(f"Something wrong with url: {url} with error: {e}", flush=True)
         time.sleep(1)
      print(f"Valid Server: {str(getValidServers())}", flush=True)
      time.sleep(interval)

