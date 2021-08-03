# Copyright 2018 Google LLC
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

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask
from urllib.request import Request, urlopen
import re

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/scrape')
def scrape():
    url = 'https://allocation.miq.govt.nz/portal/'
    #TODO Rotate id
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0'
    req = Request(url, headers={'User-Agent': agent})
    html_bytes = urlopen(req).read()
    html = html_bytes.decode("utf-8")
    #regex = r"<div class=\"no\" . aria-label=\"(\w+ \d+)\".+<\/div>"
    regex = r"<div(?! class=\"no\") . aria-label=\"(\w+ \d+)\".+<\/div>"
    test_str = html
    matches = re.finditer(regex, test_str, re.MULTILINE)
    s = ''
    for matchNum, match in enumerate(matches, start=1):
        s = s + match.group(1) +'<br>'
    return s

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]