import base64
from urllib.request import Request, urlopen
import re

def scrape(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    ### Get args to determine user agent and webserver
    #agent = base64.b64decode(event['UserAgent']).decode('utf-8')
    ### Send request to MIG
    #url = 'https://allocation.miq.govt.nz/portal/'
    #req = Request(url, headers={'User-Agent': agent})
    #html_bytes = urlopen(req).read()
    #html = html_bytes.decode("utf-8")
    #regex = r"<div (?!class=\"no\") . aria-label=\"(\w+ \d+)\".+<\/div>"
    #matches = re.finditer(regex, html, re.MULTILINE)
    #dates = [match.group(1) for match in matches] 
    #dates_str = ('None' if len(dates) == 0 else str(dates))
    print(pubsub_message)
    #print(agent)

#{
#"UserAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0",
#"ScraperUrl":"Muppet"
#}    
