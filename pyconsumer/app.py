import faust


app = faust.App('pyconsumer',
                broker='kafka://kafka-broker-1:19092',
                autodiscover=True,
                origin='pyconsumer')


import pyconsumer.streams.agents


def main() -> None:
    app.main()
