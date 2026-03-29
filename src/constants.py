import os

# UI
SEPARATION_WIDTH = 100

# Data
ID_PATH = os.path.join(os.path.dirname(__file__), "../digital_ids.csv")
LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs.csv")
LOG_HEADERS = ["id", "timestamp", "accepted", "organisation", "digitalID", "action", "justification", "currentValue", "newValue"]

# Digital ID field names
DIGITAL_ID_ALL_FIELDS = ["id", "status", "firstName", "surname", "dateOfBirth"]
