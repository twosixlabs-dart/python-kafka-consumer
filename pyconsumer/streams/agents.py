from faust.streams import Stream
from pyconsumer.app import app
from pyconsumer.messages.stream_message import StreamMessage


stream_out_topic = app.topic('stream.out', value_type=StreamMessage)


@app.agent(stream_out_topic)
async def stream_out(stream : Stream):
    """Print the events to stdout"""
    async for event in stream:
        event.breadcrumbs.append('python-kafka-consumer')
        print(f'event ID {event.id} with breadcrumbs {event.breadcrumbs}')
        yield event
