import sys
import os
import logging
from collections import defaultdict

# Logging configurations
logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG = logging.getLogger("log_parser")

# Constants / Defaults
INPUT_DIR = os.path.join("inputs")
OUTPUT_DIR = os.path.join("outputs")
PROTOCOL_MAPPING_CSV = "protocol-numbers-1.csv"
LOOKUP_TABLE_CSV = "lookup-table.csv"



def parse_logs(log_file, protocol_map, lookup_table):
    tag_counter = defaultdict(int)
    port_protocol_counter = defaultdict(int)
    with open(log_file, "r") as f:
        for line in f.readlines():
            # Skip empty lines if any
            if not line.strip():
                continue
            columns = line.split(" ")
            try:
                dstport, protocol_int = int(columns[6]), int(columns[7])
                protocol = protocol_map[protocol_int]
                tag = "untagged"
                if (dstport, protocol) in lookup_table:
                    tag = lookup_table[(dstport, protocol)]
                tag_counter[tag] += 1
                port_protocol_counter[(dstport, protocol)]+=1
                LOG.debug(f"({dstport}, {protocol}) -> {tag}")
            except:
                LOG.warning(f"Unable to parse line {line}")
    
    return tag_counter, port_protocol_counter

def get_protocol_mapping():
    protocol_map = {}
    protocol_file = os.path.join(INPUT_DIR, PROTOCOL_MAPPING_CSV)
    assert os.path.exists(protocol_file)
    with open(protocol_file, "r") as f:
        # Read all lines, skip the header
        for line in f.readlines()[1:]:
            if not line.strip():
                continue
            # CSV Headers are: Decimal, Keyword, Protocol, IPv6 Extension Header, Reference
            try:
                decimal, keyword = line.strip().split(",")[:2]
                decimal = int(decimal)
                if keyword:
                    # converting to lower case to make it case insensitive
                    protocol_map[decimal] = keyword.lower()
            except:
                LOG.warning(f"Unable to parse decimal {decimal}, skipping {line}")
    return protocol_map
    

def get_lookup_table():
    lookup_table = {}
    lookup_table_file = os.path.join(INPUT_DIR, LOOKUP_TABLE_CSV)
    assert os.path.exists(lookup_table_file)
    with open(lookup_table_file, "r") as f:
        # Read all lines, skip the header
        for line in f.readlines()[1:]:
            if not line.strip():
                continue
            # CSV Headers are: dstport, protocol, tag 
            try:
                dstport, protocol, tag = line.strip().split(",")
                dstport = int(dstport)
                lookup_table[(dstport,protocol.lower())] = tag
            except:
                LOG.warning(f"Unable to parse {line}, skipping")
    return lookup_table


if __name__ == "__main__":
    # If a command line argument is passed, use that as INPUT_DIR
    if len(sys.argv) > 1:
        INPUT_DIR = sys.argv[1]
    
    # Make sure that the input directory exists
    assert os.path.exists(INPUT_DIR)

    # Parse the protocol csv file to get the protocol map
    protocol_map = get_protocol_mapping()
    assert protocol_map
    LOG.debug(protocol_map)

    # Parse the lookup table csv file to get the lookup table
    lookup_table = get_lookup_table()
    assert lookup_table
    LOG.debug(lookup_table)

    for log_file in os.listdir(INPUT_DIR):
        # Filter out log files
        if not log_file.endswith(".log"):
            LOG.info(f"{log_file} is not a log file, skipping")
            continue
        
        # Parse the log file
        file = os.path.join(INPUT_DIR, log_file)
        LOG.info(f"parsing {log_file}")
        tag_counter, port_protocol_counter = parse_logs(file, protocol_map, lookup_table)
        
        out_file = os.path.join(OUTPUT_DIR, log_file.split(".")[0] + "_out.txt")
        with open(out_file, "w") as f:
            f.write("tag,count\n")
            for tag in tag_counter:
                f.write(f"{tag},{tag_counter[tag]} \n")
            f.write("------------------------------\n" )
            f.write("dstport,protocol,count\n")
            for dstport, protocol in port_protocol_counter:
                f.write(f"{dstport},{protocol},{port_protocol_counter[(dstport, protocol)]} \n")
