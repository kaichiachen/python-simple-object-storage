# start data service
for v in 100 101 102 103 104 105 106
do
    docker run -d --name "data$v" --net=obj --ip "172.32.1.$v" -v $(cd "$(dirname "$0")"; pwd)../../../:/home/distributed_obj_storage_system objsystem:latest python distributed_obj_system/backend/data/run.py
done

for v in 50
do
    docker run -d --name "api$v" --net=obj --ip "172.32.1.$v" -v $(cd "$(dirname "$0")"; pwd)../../../:/home/distributed_obj_storage_system objsystem:latest python distributed_obj_system/backend/api/run.py
done

docker run -dt --name frontend --net=obj -v $(cd "$(dirname "$0")"; pwd)../../../:/home/distributed_obj_storage_system -w /home/distributed_obj_storage_system/distributed_obj_system objsystem:latest
