import csv
import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Expected schema fields (based on docs/data_schema.md)
# We'll focus on the 'Required' fields for this basic agent
EXPECTED_FIELDS = {
    "filing_id": str,
    "timestamp": str,  # ISO 8601 datetime string
    "user_id": str,
    "region_code": str,
    "income_bracket": str,
    "filing_type": str,
    "tax_year": int,
}

# Optional fields that can also be processed if present
OPTIONAL_FIELDS = {
    "total_income": float,
    "total_deductions": float,
    "tax_owed": float,
    "refund_amount": float,
    "filing_method": str,
    "language_preference": str,
}

ALL_FIELDS = {**EXPECTED_FIELDS, **OPTIONAL_FIELDS}

class DataIngestionAgent:
    def __init__(self):
        self.raw_data = []
        self.validated_data = []
        self.rejected_records = []
        logging.info("DataIngestionAgent initialized.")

    def _validate_record(self, record_num, record):
        """
        Validates a single record against the expected schema.
        """
        # Check for missing required fields
        for field in EXPECTED_FIELDS.keys():
            if field not in record or not record[field]:
                logging.warning(f"Record {record_num}: Missing required field '{field}'. Skipping record.")
                return None, f"Missing required field '{field}'"

        validated_record = {}
        # Validate data types and convert
        for field, field_type in ALL_FIELDS.items():
            if field in record and record[field]: # Process if field exists and is not empty
                value = record[field]
                try:
                    if field == "timestamp":
                        # Attempt to parse ISO 8601 datetime
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                        validated_record[field] = value
                    elif field_type == int:
                        validated_record[field] = int(value)
                    elif field_type == float:
                        validated_record[field] = float(value)
                    else: # str
                        validated_record[field] = str(value)
                except ValueError:
                    logging.warning(f"Record {record_num}: Invalid data type for field '{field}'. Expected {field_type.__name__}, got '{value}'. Skipping record.")
                    return None, f"Invalid data type for field '{field}'"
            elif field in EXPECTED_FIELDS: # If an expected field is somehow empty after first check
                 logging.warning(f"Record {record_num}: Required field '{field}' became empty unexpectedly. Skipping record.")
                 return None, f"Empty required field '{field}'"

        return validated_record, None

    def load_data_from_csv(self, file_path):
        """
        Loads data from a CSV file, validates it, and stores valid records.
        """
        logging.info(f"Attempting to load data from CSV: {file_path}")
        self.raw_data = []
        self.validated_data = []
        self.rejected_records = []

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Workaround for potential extra empty rows if any from DictReader with list()
                self.raw_data = [row for row in reader if any(row.values())]
                logging.info(f"Successfully read {len(self.raw_data)} non-empty records from {file_path}.")

                for i, record in enumerate(self.raw_data):
                    record_num = i + 1 # User-friendly record numbering
                    validated_record, error_reason = self._validate_record(record_num, record)
                    if validated_record:
                        self.validated_data.append(validated_record)
                    else:
                        self.rejected_records.append({"record_number": record_num, "data": record, "reason": error_reason})

            logging.info(f"Data loading complete. Valid records: {len(self.validated_data)}, Rejected records: {len(self.rejected_records)}.")

        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
        except Exception as e:
            logging.error(f"An error occurred while processing {file_path}: {e}")

    def load_data_from_list(self, data_list: list[dict]):
        """
        Loads data from a list of dictionaries, validates it, and stores valid records.
        """
        logging.info(f"Attempting to load data from list of {len(data_list)} records.")
        self.raw_data = [] # Or append? For now, let's mimic load_data_from_csv behavior
        self.validated_data = []
        self.rejected_records = []

        self.raw_data = [dict(record) for record in data_list] # Store copies

        for i, record in enumerate(self.raw_data):
            record_num = i + 1 # User-friendly record numbering
            validated_record, error_reason = self._validate_record(record_num, record)
            if validated_record:
                self.validated_data.append(validated_record)
            else:
                self.rejected_records.append({"record_number": record_num, "data": record, "reason": error_reason})

        logging.info(f"Data loading from list complete. Valid records: {len(self.validated_data)}, Rejected records: {len(self.rejected_records)}.")

    def get_validated_data(self):
        """
        Returns the list of validated data records.
        """
        return self.validated_data

    def get_rejected_records_summary(self):
        """
        Returns a summary of records that were rejected during validation.
        """
        return self.rejected_records

if __name__ == '__main__':
    # Example usage:
    agent = DataIngestionAgent()

    # Example usage:
    agent = DataIngestionAgent()
    header = list(ALL_FIELDS.keys()) # Define header for dummy data creation

    # --- Test List Loading Example (CSV part removed to avoid file I/O issues in sandbox) ---
    print("\n--- Testing List Data Loading Example ---")
    dummy_list_data = [
        {"filing_id": "TXN-LST-001", "timestamp": "2023-02-01T10:00:00Z", "user_id": "USRLST001", "region_code": "US-TX", "income_bracket": "70k-120k", "filing_type": "individual", "tax_year": 2022, "total_income": 75000.0},
        {"filing_id": "TXN-LST-002", "timestamp": "2023-02-02T11:00:00Z", "user_id": "USRLST002", "region_code": "US-FL", "income_bracket": "100k-200k", "filing_type": "joint", "tax_year": 2022},
        {"filing_id": "TXN-LST-003", "timestamp": "bad_date", "user_id": "USRLST003", "region_code": "US-WA", "income_bracket": "50k-80k", "filing_type": "individual", "tax_year": 2022}, # Invalid timestamp example
        {"filing_id": "TXN-LST-004", "timestamp": "2023-02-03T12:00:00Z", "user_id": "USRLST004", "region_code": "US-GA", "income_bracket": "100k-200k", "filing_type": "individual", "tax_year": "WRONG_YEAR_TYPE"}, # Invalid tax_year type
        {"filing_id": "TXN-LST-005", "timestamp": "2023-02-04T13:00:00Z", "user_id": None, "region_code": "US-NC", "income_bracket": "40k-60k", "filing_type": "individual", "tax_year": 2022}, # Missing user_id example
    ]
    agent.load_data_from_list(dummy_list_data)
    print("\nValidated Data (from List Example):")
    for row in agent.get_validated_data():
        print(row)
    print("\nRejected Records (from List Example):")
    for rejected in agent.get_rejected_records_summary():
        print(rejected)
