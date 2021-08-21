import signal
import hashlib
import zlib
import redis
import json
import datetime
from .const import REDIS_SERVER, REDIS_PORT
from reedsolo import RSCodec, ReedSolomonError
RAID = 6
rsc = RSCodec(RAID)

import socket
MyIP = socket.gethostbyname(socket.gethostname())

class timeout:
   def __init__(self, seconds=120, errorMessage='Query timeout. Please try again'):
      self.seconds = seconds
      self.errorMessage = errorMessage

   def handleTimeout(self, signum, frame):
      raise Exception(self.errorMessage)

   def __enter__(self):
      signal.signal(signal.SIGALRM, self.handleTimeout)
      signal.alarm(self.seconds)

   def __exit__(self, type, value, traceback):
      signal.alarm(0)

def splitData(data):
   res = rsc.encode(data)
   print(res,flush=True)
   n = len(res)//RAID
   big_num = len(res)%RAID
   left_start = big_num*(n+1)

   return [res[i*(n+1):(i+1)*(n+1)] for i in range(big_num)] + [res[left_start+i*n:left_start+(i+1)*n] for i in range(0, RAID-big_num)]

def combineData(data):
   return rsc.decode(data)[0]


def sha256(data):
   return hashlib.sha256(data).hexdigest()

def sha256File(path):
   sha256_hash = hashlib.sha256()
   with open(path, 'rb') as f:
      for byte_block in iter(lambda: f.read(4096),b""):
         sha256_hash.update(byte_block)
   return sha256_hash.hexdigest()

def compress(data):
   return zlib.compress(data)

def decompress(data):
   print(data)
   return zlib.decompress(data)

heartbeatMap = {}
def recordHeartbeat(url):
   heartbeatMap[url] = datetime.datetime.now()

def getDataServers():
   prefix='172.32.1.%s'
   return [prefix % i for i in range(100,107) if (prefix%i) != MyIP]

def getValidServers():
   return [ url for url in getDataServers() \
         if url in heartbeatMap and datetime.datetime.now() - heartbeatMap[url] < datetime.timedelta(minutes=10)]

def getToken():
   return 'abc123'

class DB():

   r = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT)

   @classmethod
   def getMetadata(cls, name, version):
      for ver, data in cls.r.hgetall(name).items():
         if ver.decode() == version:
            return json.loads(data.decode())
      return {}

   @classmethod
   def getVersionList(cls, name):
      vers = []
      for ver, data in cls.r.hgetall(name).items():
         vers.append(ver.decode())
      return vers

   @classmethod
   def addMetadata(cls, name, version, h, size, locate):
      data = {
            'hash': h,
            'time': str(datetime.datetime.now()),
            'size': size,
            'locate': locate
      }
      cls.r.hset(name, version, json.dumps(data))

   @classmethod
   def removeMetadata(cls, name, version=None):
      if version:
         cls.r.hdel(name, version)
      else:
         vers = [ver.decode() for ver, data in cls.r.hgetall(name).items()]
         for ver in vers:
            cls.r.hdel(name, ver)


if __name__ == '__main__':
   DB.addMetadata('kaijia','1.2.3','abc123')
   DB.addMetadata('kaijia','1.2.4','abc123')
   print(DB.getVersionList('kaijia'))
   print(DB.getMetadata('kaijia','1.2.4'))

