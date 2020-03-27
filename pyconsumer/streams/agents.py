from faust import StreamT
from pyconsumer.app import app
from pyconsumer.messages.stream_message import StreamMessage


# create topics
stream_out_topic = app.topic('stream.out', value_type=StreamMessage)


# create an agent subscribed to the stream.out topic. this function receives
# events, updates them, and then prints the event to stdout
@app.agent(stream_out_topic)
async def stream_out(stream: StreamT):
    """Print the events to stdout"""
    async for event in stream:
        event.breadcrumbs.append('python-kafka-consumer')
        print(f'event ID {event.id} with breadcrumbs {event.breadcrumbs}')
        yield event
