import threading
import time
import requests
from queue import Queue
import datetime
import os
import random

scrapers = [
'https://australia-southeast1-miqbooking.cloudfunctions.net/tester1',
'https://australia-southeast1-miqbooking.cloudfunctions.net/tester2',
'https://australia-southeast1-miqbooking.cloudfunctions.net/tester3',
'https://australia-southeast1-miqbooking.cloudfunctions.net/tester4',
'https://australia-southeast1-miqbooking.cloudfunctions.net/tester5',
]

user_agents = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'
]

q = Queue(maxsize=5)
finished = threading.Event()
gcounter = 1
ten_start_time = datetime.datetime.now()

# Keep queueing URLS to process
def producer(queue):
    while not finished.is_set():
        time.sleep(0.01)
        if not q.full():
            agent = user_agents[random.randint(0, len(user_agents)-1)]
            scraper = scrapers[random.randint(0, len(scrapers)-1)]
            q.put({'agent': agent, 'scraper': scraper})

# Multiple consumers work on queue
def consumer(queue):
    global finished
    global gcounter
    global ten_start_time
    while not finished.is_set(): 
        if gcounter % 10 == 0:
            print('Ten in '+ str((datetime.datetime.now()-ten_start_time).total_seconds()) +' seconds')
            ten_start_time = datetime.datetime.now()
        args = queue.get()
        agent = args['agent']
        scraper = args['scraper']
        start_time = datetime.datetime.now()
        raw_response = requests.get(scraper, headers={'User-Agent': agent})
        response = raw_response.content.decode("utf-8")
        end_time = datetime.datetime.now()
        print('Pinging from ' +scraper +' T:' + str((end_time-start_time).total_seconds()) +' seconds')
        print(response)
        if 'None' not in response and not finished.is_set():
            finished.set()
            os.system('open -a Safari https://allocation.miq.govt.nz/portal/organisation/5f377e18-43bc-4d0e-a0d3-79be3a2324ec/event/MIQ-DEFAULT-EVENT/accommodation/arrival-date#step-2')
            for i in range(10):
                print('\a')
        gcounter = gcounter + 1
        queue.task_done()

def main():
    producers = threading.Thread(target=producer, args=(q,))
    producers.daemon = True
    producers.start()

    consumers = [threading.Thread(target=consumer, args=(q,))]
    for thread in consumers:
        thread.daemon = True
        thread.start()
    
    for thread in consumers:
        thread.join()

if __name__ == '__main__':
    main()