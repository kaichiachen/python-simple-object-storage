import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.utils import sha256, compress, decompress
import requests
import argparse

from utils.const import PORT

server_url = ''

def getArgParser():
   parser = argparse.ArgumentParser(description='A frontend for object storage system.', formatter_class=argparse.RawTextHelpFormatter)
   parser.add_argument('--server', default='172.32.1.50', type=str, help='Server address for object storage system.')
   parser.add_argument('--port', default=PORT, type=int, help='Server port for object storage system.')
   parser.add_argument('--type', required=True, type=str, help='uo-> upload an object. \n'
                                                               'vl-> get version list by object name. \n'
                                                               'do-> download an object\n'
                                                               'ol-> object locations')
   parser.add_argument('--version', required=False, type=str, help='Object version')
   parser.add_argument('--name', required=True, type=str, help='Object name to upload')
   parser.add_argument('--content', required=False, type=str, help='Object content to upload')
   parser.add_argument('--file', required=False, type=str, help='Absolute path for file')


   return parser.parse_args()

def uploadObject(args):
   content = args.content
   name = args.name
   file = args.file

   if not name:
      print('--name is required')
   if not content and not file:
      print('--name or --file is required')

   if file:
      content = open(file, 'r').read()
   content = compress(content.encode()) # content type will be byte after compress
   hash = sha256(content)
   size = len(content)
   chunk = 10
   idx = 0
   for i in range(0, size, chunk):
      res = requests.post(f"{server_url}/objects/{name}", files={
                                                            'obj': content[i:i+chunk],
                                                            'hash':hash,
                                                            'version': args.version,
                                                            'start': i,
                                                            'length': chunk,
                                                            'size': size})
      idx+=1
      print(f'{idx}th times upload, with chunk size: {chunk}, '
            f'totally object size: {size} and the status code: {res.status_code}')

def downloadObject(args):
   name = args.name
   version = args.version
   if not name:
      print('--name is required')
      return
   if not version:
      print('--version is required')
      return
   size = requests.get(f"{server_url}/objects/size/{name}?version={version}").json()['size']
   print(f'Size of Object: {size} bytes')
   content = b''
   start = 0
   while len(content) < size:
      try:
         content += requests.get(f"{server_url}/objects/{name}?version={version}&start={start}").content
      except KeyboardInterrupt:
         sys.exit()
      except Exception as e:
         start = len(content)
         print('Something wrong, downloading again...', e)
   try:
      print(f'Get content: {decompress(content).decode()}')
   except Exception as e:
      print(f'Something wrong: {e}')

def getVersionList(args):
   name = args.name

   if not name:
      print('--name is required')

   res = requests.get(f"{server_url}/versions/{name}")
   if res.status_code == 200:
      print(f'Version list: {res.json()}')
   else:
      print(f'Something wrong: f{res.text}')

def getObjLocation(args):
   name = args.name
   version = args.version

   if not name:
      print('--name is required')
   if not version:
      print('--version is required')

   res = requests.get(f"{server_url}/objects/locate/{name}?version={version}")
   if res.status_code == 200:
      print(f'Location list: {[locate[0] for locate in res.json()["locate"]]}')
   else:
      print(f'Something wrong: {res.text}')


def run():
   args = getArgParser()
   global server_url
   server_url = f"http://{args.server}:{args.port}"

   funcMap[args.type](args)

funcMap = {
      'uo': uploadObject,
      'vl': getVersionList,
      'do': downloadObject,
      'ol': getObjLocation,
}

if __name__ == '__main__':
   run()
