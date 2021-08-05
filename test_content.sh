PORT=${PORT:-8080}
url=${1:-'http://localhost:'$PORT}
token=${2:-''}
expected='you successfully deployed a container image to Cloud Run'
retries=10
interval=5

for i in $(seq 0 $retries); do

    html="$(curl -si $url -H "Authorization: Bearer $token")" || html=""

    if echo "$html" | grep -q "$expected"
    then
        echo "Expected content found -- site is up"
        echo "END CONTENT TEST: Success! ✅"
        exit 0
    else
        echo "Expected content not found. retrying in $interval sec..."
        sleep $interval
    fi
done

echo "Error! Expected content not found."
echo "Was looking for '$expected'; not found in:"
echo "$html"
echo "END CONTENT TEST: Fail! 💩"

exit 1
