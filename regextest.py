import datetime
import re
from urllib.request import Request, urlopen

url = 'https://allocation.miq.govt.nz/portal/'
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0'
req = Request(url, headers={'User-Agent': agent})
html_bytes = urlopen(req).read()
html = html_bytes.decode("utf-8")
start = datetime.datetime.now()
regex = r"<div (?!class=\"no\") . aria-label=\"(\w+ \d+)\".+<\/div>"
matches = re.finditer(regex, html, re.MULTILINE)
dates = [match.group(1) for match in matches]
if len(dates) > 0:
    s = 'Open Dates:\n'
    for d in dates:
        s = s + d + '\n'
    print(s)
else:
    print('No Open Dates')
end = datetime.datetime.now()
print("time:" + str(end-start))