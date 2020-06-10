import json
from pathlib import Path
from faust import Record, StreamT
from pyconsumer import config


def write_cdr(persist_dir, key, value):
    persist = Path(persist_dir) / (key + '.txt')
    value = value.dumps().decode() if isinstance(value, Record) else json.dumps(value)
    persist.write_text(value)


def create_consumer(app):
    # create topics
    stream_out_topic = app.topic(config['topic']['from'], key_type=str, value_type=str)

    # create an agent subscribed to the stream.out topic. this function
    # receives events, updates them, and then prints the event to stdout
    @app.agent(stream_out_topic)
    async def stream_out(stream: StreamT):
        """Print the events to stdout"""
        auto_commit = config['app'].get('enable_auto_commit', False)
        events = stream.events() if auto_commit else stream.noack().events()
        async for event in events:
            print(f'persisting {event.key}')
            write_cdr(config['persist.dir'], event.key, event.value)
            yield event

