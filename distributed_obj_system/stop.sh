# start data service
for v in 100 101 102 103 104 105 106
do
    docker rm "data$v" -f
done

for v in 50
do
    docker rm "api$v" -f
done

