import os
from constants import *
from utils import *
from collections import defaultdict

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
                dstport, protocol = columns[6], columns[7]
                protocol = protocol_map[protocol.strip()]
                tag = "untagged"
                if (dstport, protocol) in lookup_table:
                    tag = lookup_table[(dstport, protocol)]
                tag_counter[tag] += 1
                port_protocol_counter[(dstport, protocol)]+=1
            except Exception as e:
                LOG.debug(e)
                LOG.warning(f"Unable to parse line {line}")
    
    return tag_counter, port_protocol_counter

def generate_output(log_file, tag_counter, port_protocol_counter):
    out_file = os.path.join(OUTPUT_DIR, log_file.split(".")[0] + "_out.txt")
    with open(out_file, "w") as f:
        f.write("tag,count\n")
        for tag in tag_counter:
            f.write(f"{tag},{tag_counter[tag]} \n")
        f.write("------------------------------\n" )
        f.write("dstport,protocol,count\n")
        for dstport, protocol in port_protocol_counter:
            f.write(f"{dstport},{protocol},{port_protocol_counter[(dstport, protocol)]} \n")

if __name__ == "__main__":
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
            LOG.warning(f"{log_file} is not a log file, skipping.")
            continue
        
        # Parse the log file
        file = os.path.join(INPUT_DIR, log_file)
        tag_counter, port_protocol_counter = parse_logs(file, protocol_map, lookup_table)
        LOG.info(f"Parsed {log_file} successfully.")

        # Generate output
        generate_output(log_file, tag_counter, port_protocol_counter)
        
