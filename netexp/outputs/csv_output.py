from netexp.outputs.base_output import BaseOutput


class CsvOutput(BaseOutput):

    def __init__(self, filename: str):
        self.header_written = False
        self.filename = filename
        self.csv_file = open(filename, 'w+')

    def send(self, packet_info: any):
        if not self.header_written:
            self.write_header(packet_info)

        self.write_record(packet_info)

    def write_record(self, packet_info: any):
        packet_info_line = ','.join([str(value) for value in packet_info.to_dict().values()])

        self.csv_file.write(packet_info_line + '\n')

    def write_header(self, packet_info: any):
        packet_info_line = ','.join(packet_info.to_dict().keys())

        self.csv_file.write(packet_info_line + '\n')
        self.header_written = True
