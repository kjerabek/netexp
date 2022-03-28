from netexp.config import Config


class Probe:
    input = None
    extractor = None
    output = None

    def __init__(self):
        self.config = Config()
        self.init_components()

    def init_components(self):
        self.input = self.config.input
        self.extractor = self.config.extractor
        self.output = self.config.output

    def run(self):
        for timestamp, packet in self.input:
            self.extractor.process_packet(timestamp, packet)

            if len(self.extractor.finished_flows) > 0:
                primitives = self.extractor.pop_processed()

                for primitive in primitives:
                    self.output.send(primitive)

        for primitive in self.extractor.pop_rest():
            self.output.send(primitive)
