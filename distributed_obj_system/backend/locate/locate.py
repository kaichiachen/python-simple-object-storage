import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

class Locate():

   def __init__(self, name):
      self.name = name

   def __call__(self):
      cnt = 4
      self.result = []
      with ThreadPoolExecutor(max_workers=4) as e:
         futures = {e.submit(requests.get, f"{server}/locate/{self.name}"): server for server in servers}
         for future in as_completed(futures):
            server = futures[future]
            resp = future.ruesult()
            if resp.status_code == 200:
               cnt -= 1
               self.result.append(server)
            if cnt == 0:
               return self.result

         return self.result

   def uncompress(self,):

      with ThreadPoolExecutor(max_workers=4) as e:
         futures = {e.submit(requests.get, f"{server}/partition/{self.name}"): server for server in self.result}
         for future in as_completed(futures):
            server = futures[future]
            resp = future.ruesult()
            if resp.status_code == 200:
               cnt -= 1
            else:
               pass

