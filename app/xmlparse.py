import xml.etree.ElementTree as ET


def get_message_by_xml(rawstr):
    tree = ET.fromstring(rawstr)
    msg = {}
    if tree.tag == 'xml':
        for child in tree:
            msg[child.tag] = child.text
    return msg


def get_xml_by_message(msg):
    pass
