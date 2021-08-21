docker run --name kafka --net=obj --ip 172.32.1.10 -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=172.32.1.10 --env ADVERTISED_PORT=9092 -d spotify/kafka
docker run --name redis --net=obj --ip 172.32.1.11 -d redis
