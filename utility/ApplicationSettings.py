import xml.etree.ElementTree


class ApplicationSettings:
    def __init__(self):
        self.settings_file = "config/ApplicationSettings.xml"
        self.settings = {}

        self.read_xml()

    def read_xml(self):
        for setting in xml.etree.ElementTree.parse(self.settings_file).getroot():
            self.settings[setting.tag] = setting.text
