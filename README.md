# python-simple-object-storage

---
### Environment Installation
pip install -r requirements.txt
docker network create --subnet=172.32.0.0/16 obj

---
### Simple object storage system
python frontend.py --name 'obj01' --content 'helloworld'
cat /tmp/objs/obj01

---
### distributed object storage system
Build object system image
```
docker build -t objsystem:latest .
```
Deploy middle ware
```
./distributed_obj_system/build_middleware/start.sh
```
Deploy object storage system
```
./distributed_obj_system/build_containers/start.sh
```
upload an object file to server
```
#> python frontend.py --type uo --name obj01 --version 1.7.3 --content 'helloworld'
1th times upload, with chunk size: 10, totally object size: 18 and the status code: 201
2th times upload, with chunk size: 10, totally object size: 18 and the status code: 200
```
download object from server
```
#> python frontend.py --type do --name obj01 --version 1.7.3
Size of Object: 19 bytes
Get content: helloworld
```
get object locations
```
#> python frontend.py --type ol --name obj01 --version 1.7.3
Location list: ['172.32.1.100', '172.32.1.106', '172.32.1.104', '172.32.1.101', '172.32.1.103', '172.32.1.105']
```
get version list of object
```
#> python frontend.py --type vl --name obj01
Version list: {'versions': ['1.7.2', '1.7.3']}
```
