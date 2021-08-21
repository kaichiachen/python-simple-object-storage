import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utils.const import PORT
from flask import Flask, request, make_response, jsonify
from markupsafe import escape

app = Flask(__name__)
DIR_PATH = ''

@app.route("/<obj_name>", methods=['GET', 'POST'])
def handler(obj_name):
   if request.method == 'GET':
      f = open(os.path.join(DIR_PATH, f"{escape(obj_name)}"), 'r')
      body = {'success':True}
      body['content'] = ''.join(f.readlines())
      return make_response(jsonify(body), 200)
   elif request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(DIR_PATH, f"{escape(obj_name)}"))
      return make_response(jsonify({'success':True}), 200)
   else:
      return make_response(jsonify({'success':False, 'reason': f'Method({request.method}) not found'}), 404)

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
