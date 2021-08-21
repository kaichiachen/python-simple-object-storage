import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.utils import sha256, compress
import requests
import argparse

from utils.const import PORT

server_url = ''

def getArgParser():
   parser = argparse.ArgumentParser(description='A frontend for object storage system.', formatter_class=argparse.RawTextHelpFormatter)
   parser.add_argument('--server', default='localhost', type=str, help='Server address for object storage system.')
   parser.add_argument('--port', default=PORT, type=int, help='Server port for object storage system.')
   parser.add_argument('--type', required=True, type=str, help='uo-> upload an object. \n'
                                                               'vl-> get version list by object name. \n'
                                                               'do-> download an object\n')
   parser.add_argument('--version', required=False, type=str, help='Object version')
   parser.add_argument('--name', required=True, type=str, help='Object name to upload')
   parser.add_argument('--content', required=False, type=str, help='Object content to upload')
   parser.add_argument('--file', required=False, type=str, help='Absolute path for file')


   return parser.parse_args()

def uploadObject(args):
   content = args.content
   name = args.name

   content = compress(content.encode()) # content type will be byte after compress
   hash = sha256(content)
   size = len(content)
   chunk = 10
   for i in range(0, size, chunk):
      res = requests.post(f"{server_url}/objects/{name}", files={
                                                            'obj': content[i:i+chunk],
                                                            'hash':hash,
                                                            'version': args.version,
                                                            'start': i,
                                                            'length': chunk,
                                                            'size': size})
      print(i, chunk, size, res.status_code)

def downloadObject(args):
   size = requests.get(f"{server_url}/objects/size/{name}").json()['size']
   print(f'Size of Object: {size} bytes')
   content = ''
   while len(content)<size:
      content += requests.get(f"{server_url}/objects/{name}").text

   print(f'Content get: {content}')


def getVersionList(args):
   name = args.name

   res = requests.get(f"{server_url}/versions/{name}")
   print(f'Version list: {res.json()}')

def run():
   args = getArgParser()
   global server_url
   server_url = f"http://{args.server}:{args.port}"

   funcMap[args.type](args)

funcMap = {
      'uo': uploadObject,
      'vl': getVersionList,
      'do': downloadObject
}

if __name__ == '__main__':
   run()
