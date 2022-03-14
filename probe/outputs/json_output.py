from probe.outputs.base_output import BaseOutput


class JsonOutput(BaseOutput):

    def __init__(self, filename: str):
        self.filename = filename
        self.json_file = open(filename, 'w+')
        self.json_file.write('[')

    def send(self, packet_info: any):
        self.write_record(packet_info)

    def write_record(self, packet_info: any):
        json_string = packet_info.to_json()

        self.json_file.write(json_string + ',')

    def __del__(self):
        self.json_file.write(']')
