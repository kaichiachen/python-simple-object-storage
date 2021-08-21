import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))
from utils.utils import DB, splitData, combineData, getDataServers
from utils.const import KAFKA_SERVICE, KAFKA_PORT, PORT
from kafka import KafkaProducer
import random
import pickle
import requests

class Producer():

   instance = None

   def __init__(self):
      self.producer = KafkaProducer(bootstrap_servers=[f"{KAFKA_SERVICE}:{KAFKA_PORT}"], value_serializer=lambda v: pickle.dumps(v))

   @classmethod
   def getInstance(cls):
      if not cls.instance:
         cls.instance = Producer()
      return cls.instance

   def isConnected(self):
      return self.producer != None

   def send(self, topic, value):
      print(f'Producer send to server {topic} with value {value}', flush=True)
      res = self.producer.send(topic, value=value)
      cnt = 5
      while cnt >= 0:
         if res.succeeded():
            return True
      return False

def produce_object(content):
   if 'name' not in content:
      return False
   size = len(content['obj'])
   components = splitData(content['obj'])
   servers = getDataServers()
   locats = []
   for i, comp in enumerate(components):
      while servers:
         idx = random.randint(0,len(servers)-1)
         server = servers[idx]
         res = Producer.getInstance().send(server, value={f"{content['hash']}-{i}": comp})
         if res:
            locats.append((server, i, len(comp)))
            break

      del servers[idx]

   if len(locats) == len(components):
      DB.addMetadata(f"{content['name']}", content['version'], content['hash'], size, locats)
      return True
   else:
      print(f"Numer of components: {num(components)} and number of locates: {len(locats)} are not match.", flush=True)

   return False

def getObj(name, version):
   metadata = DB.getMetadata(name, version)
   hash = metadata['hash']
   dataSize = metadata['size']
   locate = metadata['locate']
   locate.sort(key=lambda x: x[1]) # x[1] is idx

   data = b''
   for server, idx, size in locate:
      try:
         res = requests.get(f"http://{server}:{PORT}/partition/{hash}-{idx}", timeout=1)
         if res.status_code == 201:
            return -1
         else:
            data += res.content
      except Exception as e:
         print('request error: %s' % e, flush=True)
         data += b'x'*size
   print(data, flush=True)
   try:
      res = combineData(data)
      return res
   except:
      return -2

