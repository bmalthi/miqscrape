# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Echo commands
set -v

# [START getting_started_gce_startup_script]
# Install Stackdriver logging agent
curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
sudo bash install-logging-agent.sh

# Install or update needed software
apt-get update
apt-get install -yq git supervisor python python-pip python3-pip
#pip install --upgrade pip virtualenv
pip3 install --upgrade pip virtualenv

# Account to own server process
useradd -m -d /home/pythonapp pythonapp

# Get Github public key from secret manager
#gcloud secrets versions access 1 --secret="github_key" --format='get(payload.data)' | tr '_-' '/+' | base64 -d > ~/.ssh/id_github
#mkdir /root/.ssh
#gcloud secrets versions access 1 --secret="github_key" --format='get(payload.data)' | tr '_-' '/+' | base64 -d > /root/.ssh/id_github
#chmod 400 /root/.ssh/id_github
#eval "$(ssh-agent -s)"
#ssh-add -k /root/.ssh/id_github

# Fetch source code
export HOME=/root
#git clone git@github.com:bmalthi/miqscrape.git /opt/app
gcloud source repos clone github_bmalthi_miqscrape /opt/app
cd /opt/app
git checkout main
ls

# Yolo Step
export BASH_SOURCE-=yolo

# Python environment setup
virtualenv -p python3 /opt/app/env
ls
source /opt/app/env/bin/activate
/opt/app/env/bin/pip3 install -r /opt/app/requirements.txt

# Set ownership to newly created account
chown -R pythonapp:pythonapp /opt/app

# Put supervisor configuration in proper place
cp /opt/app/python-app.conf /etc/supervisor/conf.d/python-app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update
# [END getting_started_gce_startup_script]