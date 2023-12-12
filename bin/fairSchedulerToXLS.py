import xml.etree.ElementTree as ET
import pandas as pd
import re
import argparse


def parse_users(elem):
    """Capture user elements and return a list of user dictionaries."""
    users = []
    if elem.tag == 'user':
        user = {'name': elem.attrib.get('name')}
        max_running_apps = elem.find('maxRunningApps')
        if max_running_apps is not None:
            user["maxRunningApps"] = max_running_apps.text
        users.append(user)
    for child in elem:
        users.extend(parse_users(child))
    return users


def parse_queues(elem, parent_name=''):
    """Capture queue elements from xml and return a list of dictionaries."""
    queues = []
    if elem.tag == 'queue':
        queue = {'name': elem.attrib.get('name'), 'parent': parent_name}
        for child in elem:
            if child.tag != 'queue':  # add non-queue child data
                queue[child.tag] = child.text
            else:
                # For nested queues, perform recursive parsing
                queues.extend(parse_queues(child, parent_name=elem.attrib.get('name')))
        queues.append(queue)
    return queues


def parse_queue_resources(elem):
    """Currently this function is targeting capture of Max, Min, Memory, Vcores and Weights to compile into
       one Tab in the xlsx file. """
    queue_resources = []
    if elem.tag == 'queue':
        queue_resource = {'name': elem.attrib.get('name')}
        max_resources = elem.find('maxResources')
        min_resources = elem.find('minResources')
        weight = elem.find('weight')
        if max_resources is not None:
            resources_split = max_resources.text.split(',')
            queue_resource['maxMemory'] = resources_split[0].strip()
            queue_resource['maxVcores'] = resources_split[1].strip() if len(resources_split) > 1 else None
        if min_resources is not None:
            resources_split = min_resources.text.split(',')
            queue_resource['minMemory'] = resources_split[0].strip()
            queue_resource['minVcores'] = resources_split[1].strip() if len(resources_split) > 1 else None
        if weight is not None:
            queue_resource['weight'] = weight.text
        queue_resources.append(queue_resource)
    for child in elem:
        queue_resources.extend(parse_queue_resources(child))
    return queue_resources


# Calculate_totals tallies up the total MaxMemory and MaxVcores. Not sure if this is useful information.
# So this is included in the scripted but currently commented out in execution.
def calculate_totals(queue_resources_data):
    total_memory, total_vcores = 0, 0
    memory_pattern = re.compile(r'(\d+) mb')
    vcores_pattern = re.compile(r'(\d+) vcores')

    for resource in queue_resources_data:
        memory_match = memory_pattern.search(resource.get('maxMemory', ''))
        vcores_match = vcores_pattern.search(resource.get('maxVcores', ''))

        if memory_match:
            total_memory += int(memory_match.group(1))
        if vcores_match:
            total_vcores += int(vcores_match.group(1))

    return {'name': 'Total', 'maxMemory': f'{total_memory} mb', 'maxVcores': f'{total_vcores} vcores', 'weight': ''}


# Parsing out the schedular xml into User_Data, Queue_Data, Queue_resources.
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    users_data, queues_data, queue_resources_data = [], [], []
    for elem in root:
        users_data.extend(parse_users(elem))
        queues_data.extend(parse_queues(elem))
        queue_resources_data.extend(parse_queue_resources(elem))

    queue_resources_data = parse_queue_resources(root)
    # Optional call to cacluated the total resources from the maxMemory and maxVcores Columns.
    # queue_resources_totals = calculate_totals(queue_resources_data)
    # queue_resources_data.append(queue_resources_totals)

    return users_data, queues_data, queue_resources_data


# Write data to Excel in different sheets
def write_to_excel(users_data, queues_data, queue_resources_data, excel_file):
    with pd.ExcelWriter(excel_file) as writer:
        pd.DataFrame(queue_resources_data).to_excel(writer, sheet_name='Queue Resources', index=False)
        pd.DataFrame(users_data).to_excel(writer, sheet_name='Users', index=False)
        pd.DataFrame(queues_data).to_excel(writer, sheet_name='Queues', index=False)


# Main execution

def main():
    # Command Help and argument parser.
    #  fairSchedulerToXLS.py [-h] -x XML_FILE -o EXCEL_FILE

    commandparser = argparse.ArgumentParser(description="Parse YARN Fair Scheduler XML and output to Excel.")
    commandparser.add_argument("-x", "--xml", dest="xml_file", required=True,
                               help="Path to the Fair Scheduler XML file")
    commandparser.add_argument("-o", "--output", dest="excel_file", required=True,
                               help="Path for the output Excel file")

    userargs = commandparser.parse_args()

    # Capture the XML elements.
    users_data, queues_data, queue_resources_data = parse_xml(userargs.xml_file)
    # Store XML elements into tabbed spreadsheet.
    write_to_excel(users_data, queues_data, queue_resources_data, userargs.excel_file)


if __name__ == "__main__":
    main()
