set -ex

#gcloud config set project miqscrape
MY_INSTANCE_NAME="scrapee3"
ZONE=australia-southeast1-a

gcloud compute instances create $MY_INSTANCE_NAME \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=g1-small \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=/home/bmalthi/github/miqscrape/startup_script.sh \
    --zone $ZONE \
    --tags http-server

gcloud compute firewall-rules create default-allow-http-8080 \
    --allow tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 8080 access to http-server"

gcloud compute instances get-serial-port-output $MY_INSTANCE_NAME --zone $ZONE    