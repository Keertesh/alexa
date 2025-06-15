# Tax Analysis Multi-Agent System

This project is a multi-agent system designed for real-time analysis of tax filing data. It aims to detect trends, make predictions, identify influencing factors, generate insights, simulate policy changes, and support multiple languages.

## How to Run

The primary way to run the agent currently is by executing the `src/agents/data_ingestion_agent.py` script directly.

Command to run the script:
```bash
python src/agents/data_ingestion_agent.py
```

This will run the example usage included in that script.

**Note:** Python 3.x is expected.

## Running the Demo

The `src/demo.py` script provides a clear example of how to use the `DataIngestionAgent` to load and validate data. It showcases how the agent processes a list of records, separating valid data from records that fail validation due to incorrect types, formats, or missing fields.

Command to run the demo:
```bash
python src/demo.py
```

### Expected Output

When you run `src/demo.py`, the console output should look similar to this:

```
Validated Data (from Demo):
{'id': 1, 'name': 'John Doe', 'age': 30, 'email': 'john.doe@example.com'}
{'id': 4, 'name': 'Bob Green', 'age': 22, 'email': 'bob.green@example.com'}
{'id': 5, 'name': 'Charlie Black', 'age': 35, 'email': 'charlie.black@example.com'}
{'id': 9, 'name': 'Grace Pink', 'age': 50, 'email': 'grace.pink@example.com'}
{'id': 10, 'name': 'Henry Yellow', 'age': 60, 'email': 'henry.yellow@example.com'}
{'id': 1, 'name': 'Duplicate ID', 'age': 45, 'email': 'duplicate.id@example.com'}
{'id': 14, 'name': 'Olivia Purple', 'age': 27, 'email': 'olivia.purple@example.com'}

Rejected Records (from Demo):
{'original_record_index': 1, 'record_data': {'id': 2, 'name': 'Jane Smith', 'age': 'twenty-five', 'email': 'jane.smith@example.com'}, 'errors': ["Invalid data type for field 'age': Expected <class 'int'> but got <class 'str'>."]}
{'original_record_index': 2, 'record_data': {'id': 3, 'name': 'Alice Brown', 'age': 40, 'email': 'alice.brown'}, 'errors': ["Invalid email format for field 'email': alice.brown."]}
{'original_record_index': 5, 'record_data': {'id': 6, 'name': 'David White', 'age': -5, 'email': 'david.white@example.com'}, 'errors': ["Invalid value for field 'age': Must be positive."]}
{'original_record_index': 6, 'record_data': {'id': 7, 'name': 'Eve Blue', 'age': 28, 'email': 'eve.blue@example'}, 'errors': ["Invalid email format for field 'email': eve.blue@example."]}
{'original_record_index': 7, 'record_data': {'id': 8, 'name': 'Frank Red', 'age': 'unknown', 'email': 'frank.red@example.com'}, 'errors': ["Invalid data type for field 'age': Expected <class 'int'> but got <class 'str'>."]}
{'original_record_index': 10, 'record_data': {'id': 11, 'age': 33, 'email': 'missing.name@example.com'}, 'errors': ["Missing required field: 'name'."]}
{'original_record_index': 11, 'record_data': {'id': 12, 'name': 'Missing Email', 'age': 29}, 'errors': ["Missing required field: 'email'."]}
{'original_record_index': 12, 'record_data': {'id': 13, 'name': 'Missing Age', 'email': 'missing.age@example.com'}, 'errors': ["Missing required field: 'age'."]}
```
