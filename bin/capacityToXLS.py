import xml.etree.ElementTree as ET
import pandas as pd
import argparse

def parse_properties(elem):
    """Parse property elements and return a list of dictionaries."""
    properties = []
    for prop in elem.findall('property'):
        name = prop.find('name').text if prop.find('name') is not None else ''
        value = prop.find('value').text if prop.find('value') is not None else ''
        properties.append({'name': name, 'value': value})
    return properties

def separate_queue_properties(properties):
    """Separate queue-specific properties into a different list."""
    queue_props = [prop for prop in properties if 'yarn.scheduler.capacity.root.' in prop['name']]
    general_props = [prop for prop in properties if 'yarn.scheduler.capacity.root.' not in prop['name']]
    return general_props, queue_props


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    properties = parse_properties(root)
    general_properties, queue_properties = separate_queue_properties(properties)

    # Sort queue properties by name
    def function(x):
        return x['name']

    queue_properties.sort(key=function)

    return general_properties, queue_properties


# Function to write data to Excel in different sheets
def write_to_excel(general_properties, queue_properties, excel_file):
    with pd.ExcelWriter(excel_file) as writer:
        pd.DataFrame(queue_properties).to_excel(writer, sheet_name="Capacity Queue Properties", index=False)
        pd.DataFrame(general_properties).to_excel(writer, sheet_name="General Properties", index=False)
        

def main():

    commandparser = argparse.ArgumentParser(description="Parse YARN Capacity Scheduler XML and output to Excel.")
    commandparser.add_argument("-x", "--xml", dest="xml_file", required=True, help="Path to the Capacity Scheduler XML file")
    commandparser.add_argument("-o", "--output", dest="excel_file", required=True, help="Path for the output Excel file")
    
    userargs = commandparser.parse_args()

    general_properties, queue_properties = parse_xml(userargs.xml_file)
    write_to_excel(general_properties, queue_properties, userargs.excel_file)

if __name__ == "__main__":
    main()