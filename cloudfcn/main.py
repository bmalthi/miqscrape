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
    if request.args and 'user_agent' in request.args:
        raw_agent = request.args.get('user_agent')
        agent = raw_agent
    else:
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0'
    if request.args and 'master_url' in request.args:
        raw_master_url = request.args.get('master')
        master_url = raw_master_url
    else:
        master_url = 'http://222.153.101.43:9278'
    ### Send request to MIG
    url = 'https://allocation.miq.govt.nz/portal/'
    req = Request(url, headers={'User-Agent': agent})
    html_bytes = urlopen(req).read()
    html = html_bytes.decode("utf-8")
    regex = r"<div (?!class=\"no\") . aria-label=\"(\w+ \d+)\".+<\/div>"
    matches = re.finditer(regex, html, re.MULTILINE)
    dates = [match.group(1) for match in matches] 
    dates_str = ('None' if len(dates) == 0 else str(dates))
    ### Add Pub Sub
    # pushpubsub(dates_str)
    ### Ping Server with result
    # Not needed, since server gets response object anyway
    # dates_encode = urllib.parse.quote_plus(dates_str)
    # req = Request('http://222.153.101.43:9278?dates='+dates_encode, headers={'User-Agent': agent})    
    ### Return result
    return dates_str

def pushpubsub(message):
    project_id = "miqbooking"
    topic_id = "miqdate"
    publisher = pubsub_v1.PublisherClient(batch_settings=pubsub_v1.types.BatchSettings(max_messages=1))
    topic_path = publisher.topic_path(project_id, topic_id)
    # Data must be a bytestring
    data = message.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)