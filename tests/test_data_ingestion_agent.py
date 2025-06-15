import unittest
import os
import csv
import logging
from src.agents.data_ingestion_agent import DataIngestionAgent, EXPECTED_FIELDS, OPTIONAL_FIELDS

# Disable most logging for tests to keep output clean, enable critical only
logging.disable(logging.CRITICAL)

ALL_FIELDS_TEST = {**EXPECTED_FIELDS, **OPTIONAL_FIELDS}
# Create a fully populated dictionary template for a valid record
# Values are just placeholders of the correct type or format.
BASE_VALID_RECORD_TEMPLATE = {
    "filing_id": "FID001",
    "timestamp": "2023-01-01T00:00:00Z",
    "user_id": "USR001",
    "region_code": "RC1",
    "income_bracket": "B1",
    "filing_type": "individual",
    "tax_year": 2022,
    "total_income": 50000.0,
    "total_deductions": 5000.0,
    "tax_owed": 4500.0,
    "refund_amount": None,
    "filing_method": "online",
    "language_preference": "en",
}

class TestDataIngestionAgent(unittest.TestCase):

    def setUp(self):
        """Setup method for tests."""
        self.agent = DataIngestionAgent()
        self.test_files_to_cleanup = []

    def tearDown(self):
        """Teardown method to remove dummy CSV files."""
        for file_path in self.test_files_to_cleanup:
            if os.path.exists(file_path):
                os.remove(file_path)

    def _create_dummy_csv(self, file_name, data_rows, header=None):
        """Helper function to create a CSV file with given data in tests/ directory."""
        if header is None:
            header = list(ALL_FIELDS_TEST.keys())

        # Ensure tests directory exists
        if not os.path.exists("tests"):
            os.makedirs("tests")

        file_path = os.path.join("tests", file_name)

        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            # Ensure all rows are dictionaries
            dict_rows = []
            for row_data in data_rows:
                if isinstance(row_data, dict):
                    dict_rows.append(row_data)
                elif isinstance(row_data, list): # if data is passed as list of values
                    dict_rows.append(dict(zip(header, row_data)))
                else:
                    raise ValueError("Unsupported row format in _create_dummy_csv")
            writer.writerows(dict_rows)
        self.test_files_to_cleanup.append(file_path)
        return file_path

    # --- Tests using direct list input ---

    def test_load_valid_data_from_list(self):
        """Test loading a list with all valid records."""
        valid_data = [
            {**BASE_VALID_RECORD_TEMPLATE, "filing_id": "LID001", "tax_year": 2022, "total_income": 60000.0},
            {**BASE_VALID_RECORD_TEMPLATE, "filing_id": "LID002", "user_id": "USR002", "tax_year": 2023, "total_income": 70000.0, "refund_amount": 500.0, "tax_owed": None},
        ]
        self.agent.load_data_from_list(valid_data)

        self.assertEqual(len(self.agent.get_validated_data()), 2)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 0)
        self.assertIsInstance(self.agent.get_validated_data()[0]['tax_year'], int)
        self.assertIsInstance(self.agent.get_validated_data()[0]['total_income'], float)
        self.assertEqual(self.agent.get_validated_data()[0]['filing_id'], "LID001")

    def test_load_list_with_missing_required_fields(self):
        """Test loading list data where some records miss required fields."""
        data_with_missing = [
            {**BASE_VALID_RECORD_TEMPLATE, "filing_id": "LID003"}, # Valid
            {**{k: v for k, v in BASE_VALID_RECORD_TEMPLATE.items() if k != "user_id"}, "filing_id": "LID004"}, # user_id is missing
        ]
        self.agent.load_data_from_list(data_with_missing)

        self.assertEqual(len(self.agent.get_validated_data()), 1)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 1)
        self.assertEqual(self.agent.get_validated_data()[0]['filing_id'], "LID003")
        rejected_record = self.agent.get_rejected_records_summary()[0]
        self.assertEqual(rejected_record['data']['filing_id'], "LID004")
        self.assertIn("Missing required field 'user_id'", rejected_record['reason'])

    def test_load_list_with_invalid_types(self):
        """Test loading list data with incorrect data types for some fields."""
        data_with_invalid_types = [
            {**BASE_VALID_RECORD_TEMPLATE, "filing_id": "LID005"}, # Valid
            {**BASE_VALID_RECORD_TEMPLATE, "filing_id": "LID006", "tax_year": "INVALID_YEAR"}, # tax_year is not int
        ]
        self.agent.load_data_from_list(data_with_invalid_types)

        self.assertEqual(len(self.agent.get_validated_data()), 1)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 1)
        self.assertEqual(self.agent.get_validated_data()[0]['filing_id'], "LID005")
        rejected_record = self.agent.get_rejected_records_summary()[0]
        self.assertEqual(rejected_record['data']['filing_id'], "LID006")
        self.assertIn("Invalid data type for field 'tax_year'", rejected_record['reason'])

    def test_load_list_invalid_timestamp(self):
        """Test loading list data with an invalid ISO timestamp."""
        data_with_invalid_timestamp = [
            {**BASE_VALID_RECORD_TEMPLATE, "filing_id": "LID007"}, # Valid
            {**BASE_VALID_RECORD_TEMPLATE, "filing_id": "LID008", "timestamp": "NOT-A-VALID-DATE"},
        ]
        self.agent.load_data_from_list(data_with_invalid_timestamp)

        self.assertEqual(len(self.agent.get_validated_data()), 1)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 1)
        rejected_record = self.agent.get_rejected_records_summary()[0]
        self.assertIn("Invalid data type for field 'timestamp'", rejected_record['reason'])

    # --- Tests for CSV file loading ---

    def test_load_valid_data_from_csv(self):
        """Test loading a CSV with all valid records."""
        # Prepare data using the full header derived from ALL_FIELDS_TEST for CSV
        header_for_csv = list(ALL_FIELDS_TEST.keys())
        valid_csv_rows = [
            dict(zip(header_for_csv, ["CID001", "2023-01-01T12:00:00Z", "CUSR001", "CRG1", "CB1", "CT1", 2022, 50000.0, 5000.0, 4500.0, None, "online", "en"])),
            dict(zip(header_for_csv, ["CID002", "2023-01-02T12:00:00Z", "CUSR002", "CRG2", "CB2", "CT2", 2023, 150000.0, 15000.0, None, 1200.0, "paper", "fr"])),
        ]
        file_path = self._create_dummy_csv("valid_data.csv", valid_csv_rows, header=header_for_csv)
        self.agent.load_data_from_csv(file_path)

        self.assertEqual(len(self.agent.get_validated_data()), 2)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 0)
        # Check type conversion for CSV loaded data
        self.assertIsInstance(self.agent.get_validated_data()[0]['tax_year'], int)
        self.assertIsInstance(self.agent.get_validated_data()[0]['total_income'], float)
        self.assertEqual(self.agent.get_validated_data()[0]['filing_id'], "CID001")

    def test_load_non_existent_file(self):
        """Test loading a non-existent CSV file."""
        # Temporarily disable ERROR logging for this specific test to avoid expected error in output
        current_logging_level = logging.getLogger().getEffectiveLevel()
        logging.disable(logging.ERROR)

        self.agent.load_data_from_csv(os.path.join("tests", "non_existent_file.csv"))

        logging.disable(current_logging_level) # Restore logging level

        self.assertEqual(len(self.agent.get_validated_data()), 0)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 0)

    def test_empty_csv_file(self):
        """Test loading an empty CSV file (no data rows, only header)."""
        file_path = self._create_dummy_csv("empty_data.csv", [], header=list(ALL_FIELDS_TEST.keys()))
        self.agent.load_data_from_csv(file_path)
        self.assertEqual(len(self.agent.get_validated_data()), 0)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 0)

    def test_csv_with_only_header(self):
        """Test loading a CSV file that only contains the header row and no data."""
        file_path = os.path.join("tests", "only_header.csv")
        # Create a file with only header
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(ALL_FIELDS_TEST.keys()))
        self.test_files_to_cleanup.append(file_path)

        self.agent.load_data_from_csv(file_path)
        self.assertEqual(len(self.agent.get_validated_data()), 0)
        self.assertEqual(len(self.agent.get_rejected_records_summary()), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
