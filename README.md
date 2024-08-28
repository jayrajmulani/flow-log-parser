# A lightweight flow log parsing utility
## Flow Logs
VPC Flow Logs are a feature provided by cloud service providers like AWS (Amazon Web Services) that allow you to capture information about the IP traffic going to and from network interfaces in a Virtual Private Cloud (VPC). They are useful for network monitoring, security analysis, and troubleshooting.

## About this project
This utility processes flow log data by mapping each entry to a specific tag based on a lookup table. It then counts the number of occurrences of each tag and tracks the frequency of various port/protocol combinations. The lookup table assigns tags according to destination ports and protocols.

It supports parsing multiple log files from a directory `inputs`. It is assumed that all logs follow the default version (Version 2) taken from the official documention on [Flow log records](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html). It generates outputs corresponding to each log file and writes the same to an `outputs`. 

---

### Sample input file 
```log
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK 
2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK 
2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 25 49155 6 10 8000 1620140761 1620140821 ACCEPT OK 
2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 49156 6 12 9000 1620140761 1620140821 ACCEPT OK 
2 123456789012 eni-7i8j9k0l 172.16.0.101 192.0.2.203 993 49157 6 8 5000 1620140761 1620140821 ACCEPT OK 
2 123456789012 eni-6m7n8o9p 10.0.2.200 198.51.100.4 143 49158 6 18 14000 1620140761 1620140821 ACCEPT OK 
2 123456789012 eni-1a2b3c4d 192.168.0.1 203.0.113.12 1024 80 6 10 5000 1620140661 1620140721 ACCEPT OK 
2 123456789012 eni-1a2b3c4d 203.0.113.12 192.168.0.1 80 1024 6 12 6000 1620140661 1620140721 ACCEPT OK 
2 123456789012 eni-1a2b3c4d 10.0.1.102 172.217.7.228 1030 443 6 8 4000 1620140661 1620140721 ACCEPT OK 
2 123456789012 eni-5f6g7h8i 10.0.2.103 52.26.198.183 56000 23 6 15 7500 1620140661 1620140721 REJECT OK 
2 123456789012 eni-9k10l11m 192.168.1.5 51.15.99.115 49321 25 6 20 10000 1620140661 1620140721 ACCEPT OK 
2 123456789012 eni-1a2b3c4d 192.168.1.6 87.250.250.242 49152 110 6 5 2500 1620140661 1620140721 ACCEPT OK 
2 123456789012 eni-2d2e2f3g 192.168.2.7 77.88.55.80 49153 993 6 7 3500 1620140661 1620140721 ACCEPT OK 
2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 143 6 9 4500 1620140661 1620140721 ACCEPT OK 
```

### Sample output file
```
tag,count
untagged,8 
sv_p2,1 
sv_p1,2 
email,3 
------------------------------
dstport,protocol,count
49153,tcp,1 
49154,tcp,1 
49155,tcp,1 
49156,tcp,1 
49157,tcp,1 
49158,tcp,1 
80,tcp,1 
1024,tcp,1 
443,tcp,1 
23,tcp,1 
25,tcp,1 
110,tcp,1 
993,tcp,1 
143,tcp,1
```

---


### How to run?

1. Download [python](https://www.python.org/downloads/)
2. Clone Repositpry
```
git clone https://github.com/jayrajmulani/flow-log-parser.git
```
3. Ensure the below files are present:
  - `flow-log-parser/inputs/lookup-table.csv`
  - `flow-log-parser/inputs/protocol-numbers-1.csv` (Can be downloaded from [here](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml))
  - Atlease one `.log` file.
4. Run the script
```python3 log_parser.py```
5. Check the logs on terminal, all logs files will be parser, all others will be skipped:
```
> python3 .\log_parser.py
2024-08-28 11:27:07,738 - INFO - Parsed log-events-viewer-result.log successfully.
2024-08-28 11:27:07,740 - INFO - Parsed log-flows-large.log successfully.
2024-08-28 11:27:07,741 - INFO - Parsed sample.log successfully.
```
Note that the script may generate some warnings for unsupported files, versions or invalid log records:
```
2024-08-28 11:58:51,699 - WARNING - lookup-table.csv is not a log file, skipping.
2024-08-28 11:58:51,699 - WARNING - protocol-numbers-1.csv is not a log file, skipping.
2024-08-28 11:58:51,699 - WARNING - Unsupported version for line 3 vpc-abcdefab012345678 subnet-aaaaaaaa012345678 i-01234567890123456 eni-1235b8ca123456789 123456789010 IPv4 10.0.0.62 52.213.180.42 5001 43418 10.0.0.62 52.213.180.42 6 63388 1219 1566848933 1566849113 ACCEPT 1 OK
: 3, skipping.
2024-08-28 11:58:51,699 - WARNING - Unable to parse line 2 123456789012 eni-4h5i6j7k 172.16 1620140661 1620140721 ACCEPT OK 
```
6. Check the `outputs` directory, there should be one output analysis file (`.txt`) per input file that was parsed successfuly.


---

### Assumptions
1. The script only supports default version (Version 2) of flow log records. In case other versions, invalid records are present, they will be ignored (a warning will be logged.)
2. The `protocol-numbers-1.csv` file was downloaded from [here](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml). It is interesting to note that there were some formatting issues and unexpected line breaks, the file in this repository is the fixed correct file. 
3. Matching is case-insensitive. Tags are also converted to lower case for better consistency.
4. The default tag is `untagged` for records that don't match any other tag from the lookup table. 
5. In the lookup table, each port/protocol combination is uniquely mapped to a specific tag.


---

### Additional Tests / Analysis
- Downloaded VPC Flow Logs from a real AWS Environment, pre-processed them to remove sensitive information like IP addresses (replaced with `127.0.0.1`) and ran the script. 
- The inputs and outputs are available in the said `inputs` and `outputs` directories.
- Tested the original sample file by adding an invalid record and a record with version 3. 