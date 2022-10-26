from utility.ConnectionManagement import ConnectionManagement
import xml.etree.ElementTree


class MachineConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.default_scan_type = ""
        self.available_scan_types = []
        self.safety_devices = []

        self.read_config_from_file()

    def read_config_from_file(self):
        self.available_scan_types = []
        self.safety_devices = []
        config = xml.etree.ElementTree.parse(self.config_file).getroot()
        self.default_scan_type = config.find("DefaultScanType").text
        for scan_type in config.find("AvailableScanTypes").findall("ScanType"):
            self.available_scan_types.append(scan_type.text)
        for safety_device in config.find("SafetyDevices").findall("SafetyDevice"):
            self.safety_devices.append(safety_device.text)

    def read_config_from_system(self, c: ConnectionManagement):
        self.available_scan_types = []
        for scan_type in c.node_list.scan_types:
            self.available_scan_types.append(scan_type.get_value())

        print(self.available_scan_types)
