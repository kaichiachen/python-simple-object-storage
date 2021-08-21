import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from utils.const import PORT, KAFKA_SERVICE, KAFKA_PORT
from utils.utils import sha256, recordHeartbeat, getDataServers, getValidServers, MyIP
from heartbeats import sendHeartbeats
from flask import Flask, Response
from kafka import KafkaConsumer
import time
import threading
import json
import pickle

app = Flask(__name__)
DIR_PATH = ''

@app.route("/heartbeat", methods=['POST'])
def heatbeat():
   return Response(status=200)

@app.route("/partition/<comp_hash>", methods=['GET'])
def partition(comp_hash):
   t = open(os.path.join(DIR_PATH, comp_hash), 'rb')
   res = t.read()
   t.close()
   print(str(res), flush=True)
   return res

def SaveComp(name, data):
   f = open(os.path.join(DIR_PATH, name), 'wb')
   f.write(data)
   f.close()

def consumeComp():
   print(f'Consume topic: {MyIP}', flush=True)
   consumer = KafkaConsumer(MyIP, bootstrap_servers=[f"{KAFKA_SERVICE}:{KAFKA_PORT}"],
                            auto_offset_reset='earliest', enable_auto_commit=True, group_id='my-group',
                            value_deserializer=lambda x: pickle.loads(x))
   for msg in consumer:
      msg = msg.value
      name = list(msg.keys())[0]
      data = list(msg.values())[0]
      print(f'Data consumed: {name}, data: {data}', flush=True)
      SaveComp(name, data)
      time.sleep(1)

def prepareCompEnv():
   try:
      os.mkdir('/tmp/comps', 0o755)
   except Exception as e:
      # should be file exists
      print(e, flush=True)
   dir_path = os.path.join('/', 'tmp', 'comps')
   return dir_path

if __name__ == '__main__':
   DIR_PATH = prepareCompEnv()
   print(f'DIR_PATH={DIR_PATH}')
   threading.Thread(target=sendHeartbeats).start()
   threading.Thread(target=consumeComp).start()
   app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)

