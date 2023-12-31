# yarnSchedulerToExcel

Purpose of this project is to take a capacity-schedule.xml that is generated by the `yarn fs2cs` tool and convert the xml to xlsx format for admins to review. 

Follow the instruction listed for running the fs2cs tool found: https://docs.cloudera.com/cdp-private-cloud-upgrade/latest/yarn-scheduler-conversion/topics/yarn-fs2cs-conversion-utility.html to capture the capacity-scheduler.xml file as the input for this python script.

## Requirements

- Python 3.x
- argparse 
- Panda Libary

You can install the libaries using pip:

```bash
pip3 install pandas argparse
```

## Usage for fairSchedulerToXLS

```bash
usage: fairSchedulerToXLS.py [-h] -x XML_FILE -o EXCEL_FILE

Parse YARN Fair Scheduler XML and output to Excel.

optional arguments:
  -h, --help            show this help message and exit
  -x XML_FILE, --xml XML_FILE
                        Path to the Fair Scheduler XML file
  -o EXCEL_FILE, --output EXCEL_FILE
                        Path for the output Excel file
```

### Example: 

```bash
python3 fairSchedulerToXLS.py -x fair-scheduler.xml -o my-fair-scheduler.xlsx
```


## Usage for capacityToXLS

```bash
python3 capacityToXLS.py [-h] -x XML_FILE -o EXCEL_FILE

Parse YARN Capacity Scheduler XML and output to Excel.

optional arguments:
  -h, --help            show this help message and exit
  -x XML_FILE, --xml XML_FILE
                        Path to the Capacity Scheduler XML file
  -o EXCEL_FILE, --output EXCEL_FILE
                        Path for the output Excel file
```
### Example: 

```bash
python3 capacityToXLS.py -x capacity-scheduler.xml -o my-capacity-scheduler.xlsx
```





