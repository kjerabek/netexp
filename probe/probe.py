from probe import config


class Probe:
    def __init__(self):
        self.input = config.input
        self.extractor = config.extractor
        self.output = config.output

        self.run()

    def run(self):
        counter = 0

        for timestamp, packet in self.input:
            self.extractor.process_packet(timestamp, packet)

            if len(self.extractor.finished_flows) > 0:
                primitives = self.extractor.pop_processed()

                for primitive in primitives:
                    counter += 1
                    self.output.send(primitive)

        for primitive in self.extractor.pop_rest():
            self.output.send(primitive)
            counter += 1

        print('total count of flows', counter, '=================================================')
