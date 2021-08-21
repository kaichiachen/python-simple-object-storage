import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import requests
import argparse

from utils.const import PORT

def getArgParser():
   parser = argparse.ArgumentParser(description='A frontend for object storage system.')
   parser.add_argument('--server', default='localhost', type=str, help='Server address for object storage system.')
   parser.add_argument('--port', default=PORT, type=int, help='Server port for object storage system.')
   parser.add_argument('--name', required=True, type=str, help='Object name to upload')
   parser.add_argument('--content', required=True, type=str, help='Object content to upload')

   return parser.parse_args()

def run():
   args = getArgParser()

   server_url = f"http://{args.server}:{args.port}"

   res = requests.post(f"{server_url}/{args.name}", files={'file': args.content})

if __name__ == '__main__':
   run()
