import requests
import re

def scrape(request):
    """Scrapes targetted URL, and sends response to local webserver
       +adds to pubsub
       +texts user
    """
    ### Get args to determinr user agent and webserver
    agent = request.headers.get('User-Agent')
    ### Send request to MIG
    url = 'https://allocation.miq.govt.nz/portal/'
    try:
        response = requests.get(url, headers={'User-Agent': agent})
        status_code = response.status_code
        html = response.content.decode("utf-8")
        regex = r"<div (?!class=\"no\") . aria-label=\"(\w+ \d+)\".+<\/div>"
        matches = re.finditer(regex, html, re.MULTILINE)
        dates = [match.group(1) for match in matches] 
        dates_str = ('None' if len(dates) == 0 else str(dates))        
    except:
        status_code = 403
        dates_str = None
    return 'Status:' +str(status_code) +' Dates:' +dates_str