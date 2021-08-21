import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.const import PORT, KAFKA_SERVICE, KAFKA_PORT
from utils.utils import sha256File, DB
from obj import produce_object, getObj
from locate.locate import Locate
from flask import Flask, request, Response
import json

app = Flask(__name__)
DIR_PATH = ''

def get_object(obj_name):
   obj = Locate.locate(obj_name)
   ob.uncompress()

@app.route("/versions/<obj_name>", methods=['GET'])
def getVersion(obj_name):
   versions = DB.getVersionList(obj_name)
   return Response(json.dumps({'versions': versions}), status=200, mimetype='application/json')

@app.route("/objects/size/<obj_name>", methods=['GET'])
def getSize(obj_name):
   if request.method == 'GET':
      version = request.args.get('version')
      if version:
         metadata = DB.getMetadata(name, version)
         dataSize = metadata['size']
         return Response({'size': dataSize}, status=200, mimetype='application/json')

   return Response(json.dumps({'size': 0}), status=400, mimetype='application/json')


@app.route("/objects/<obj_name>", methods=['GET', 'POST'])
def handler(obj_name):
   reason = 'Unknown'
   if request.method == 'GET':
      version = request.args.get('version')
      start = request.args.get('start')
      start = start if start else 0
      if version:
         data = getObj(obj_name, version)
         data = data[start:]
         def gen():
            chunk = 10
            for i in range(0,len(data),chunk):
               yield data[i:i+chunk]
         return Response(gen(), mimetype='text/xml')
      else:
         reason = 'version not found'

   elif request.method == 'POST':
      obj = request.files['obj'].read()
      hash = request.files['hash'].read().decode()
      version = request.files['version'].read().decode()
      start = int(request.files['start'].read().decode())
      length = int(request.files['length'].read().decode())
      filesize = int(request.files['size'].read().decode())
      if start == 0:
         f = open(os.path.join(DIR_PATH, hash), 'wb')
      else:
         f = open(os.path.join(DIR_PATH, hash), 'ab')
      f.write(obj)
      f.close()

      if start+length >= filesize:
         obj_hash = sha256File(os.path.join(DIR_PATH, hash))
         if hash == obj_hash:
            if produce_object({'name': obj_name, 'version': version, 'hash': hash, 'obj': open(os.path.join(DIR_PATH, hash), 'rb').read()}):
               return Response(json.dumps({}), status=200, mimetype='application/json')
            else:
               return Response(json.dumps({}), status=400, mimetype='application/json')
         else:
            print(f"hash should be {obj_hash}", flush=True)
            reason = f"hash should be {obj_hash}"
         return Response(json.dumps({'success':False, 'reason': reason}), status=400, mimetype='application/json')

      else:
         return Response(json.dumps({}), status=201, mimetype='application/json')

def prepareObjEnv():
   try:
     os.mkdir('/tmp/objs', 0o755)
   except Exception as e:
      # should be file exists
      print(e, flush=True)

   dir_path = os.path.join('/', 'tmp', 'objs')
   return dir_path

if __name__ == '__main__':
   DIR_PATH = prepareObjEnv()
   print(f'DIR_PATH={DIR_PATH}')
   app.run(host='0.0.0.0', port=PORT, debug=True)
