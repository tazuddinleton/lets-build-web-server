start=$(($(date +%s%N)/1000000))

i=1
while [ $i -le 100 ]
do
    echo $(curl localhost:8080/folks)    
    i=$(($i+1))
done

end=$(($(date +%s%N)/1000000))

echo "total time: " $(($end-$start)) "mills"