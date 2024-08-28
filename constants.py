import os
import logging

# Constants / Defaults
INPUT_DIR = os.path.join("inputs")
OUTPUT_DIR = os.path.join("outputs")
PROTOCOL_MAPPING_CSV = "protocol-numbers-1.csv"
LOOKUP_TABLE_CSV = "lookup-table.csv"

# Logging configurations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOG = logging.getLogger("log_parser")