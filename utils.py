from constants import *

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
                if keyword:
                    # converting to lower case to make it case insensitive
                    protocol_map[decimal.strip()] = keyword.lower()
            except Exception as e:
                LOG.debug(e)
                LOG.warning(f"Unable to parse {line}, skipping")
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
                lookup_table[(dstport.strip(),protocol.lower())] = tag.lower()
            except:
                LOG.warning(f"Unable to parse {line}, skipping")
    return lookup_table