from flask import Flask, request
import os
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def receive_message():
    dates = request.args.get('dates')
    print("Received Message at:" +str(datetime.datetime.now()))
    print(dates)
    if dates != 'None':
        os.system('open -a Safari https://allocation.miq.govt.nz/portal/organisation/5f377e18-43bc-4d0e-a0d3-79be3a2324ec/event/MIQ-DEFAULT-EVENT/accommodation/arrival-date#step-2')
    return "Hello, world!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
