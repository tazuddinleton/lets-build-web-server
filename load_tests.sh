

FILE="urls.txt"
if [ ! -e $FILE ]
then    
    read N    
    url="http://localhost:8080/hello"
    n=1
    while [ $n -le $N ]
    do
        echo "url = $url" >> urls.txt
        n=$(($n+1))    
    done
fi

echo $(curl --parallel --parallel-immediate --parallel-max 10 --config urls.txt)