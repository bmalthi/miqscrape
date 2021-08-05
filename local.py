from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import datetime
#os.system('open -a Safari https://allocation.miq.govt.nz/portal/organisation/5f377e18-43bc-4d0e-a0d3-79be3a2324ec/event/MIQ-DEFAULT-EVENT/accommodation/arrival-date#step-2')

project_id = "miqbooking"
subscription_id = "miqdate-pull"
timeout = 360

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

#miq-date-pull-account@miqbooking.iam.gserviceaccount.com

start_time = str(datetime.datetime.now())

def callback(message):
    receive_time = str(datetime.datetime.now())
    print(f"Received {message}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

#export GOOGLE_APPLICATION_CREDENTIALS="/Users/bmalthi/miqbooking-71934817a6f0.json"