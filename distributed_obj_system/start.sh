# start data service
for v in 100 101 102 103 104 105 106
do
    docker run -d --name "data$v" --net=obj --ip "172.32.1.$v" -v /Users/ckaijia/Desktop/object_storage:/home/object_storage myobj:api python 7.\ data\ compression/backend/data/run.py
done

for v in 50
do
    docker run -d --name "api$v" --net=obj --ip "172.32.1.$v" -v /Users/ckaijia/Desktop/object_storage:/home/object_storage myobj:api python 7.\ data\ compression/backend/api/run.py
done

