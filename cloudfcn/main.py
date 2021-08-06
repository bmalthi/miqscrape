from urllib.request import Request, urlopen
import urllib.parse
import re
#from google.cloud import pubsub_v1

def scrape(request):
    """Scrapes targetted URL, and sends response to local webserver
       +adds to pubsub
       +texts user
    """
    ### Get args to determinr user agent and webserver
    agent = request.headers.get('User-Agent')
    ### Send request to MIG
    url = 'https://allocation.miq.govt.nz/portal/'
    req = Request(url, headers={'User-Agent': agent})
    response = urlopen(req)
    html = response.read().decode("utf-8")
    status_code = response.getcode()
    regex = r"<div (?!class=\"no\") . aria-label=\"(\w+ \d+)\".+<\/div>"
    matches = re.finditer(regex, html, re.MULTILINE)
    dates = [match.group(1) for match in matches] 
    dates_str = ('None' if len(dates) == 0 else str(dates))
    ### Add Pub Sub
    # pushpubsub(dates_str)
    ### Return result
    return str(status_code)+'\n'+dates_str

#def pushpubsub(message):
#    project_id = "miqbooking"
#    topic_id = "miqdate"
#    publisher = pubsub_v1.PublisherClient(batch_settings=pubsub_v1.types.BatchSettings(max_messages=1))
#    topic_path = publisher.topic_path(project_id, topic_id)
#    # Data must be a bytestring
#    data = message.encode("utf-8")
#    # When you publish a message, the client returns a future.
#    future = publisher.publish(topic_path, data)